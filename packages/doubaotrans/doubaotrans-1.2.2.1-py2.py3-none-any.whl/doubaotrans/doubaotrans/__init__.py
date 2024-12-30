import os
from dotenv import load_dotenv
import openai
from typing import List, Union, Dict, Optional, Tuple, Any
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from langdetect import detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from pathlib import Path
import re
import uuid
import asyncio
import aiohttp
import httpx
import threading
try:
    from collections.abc import MutableSet
except ImportError:
    from collections import MutableSet

# 首先定义常量
DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "ep-20241114093010-dm56w"
MAX_RETRIES = 3
MAX_WORKERS = 5  # 并发线程数

# 自定义异常类
class DoubaoError(Exception):
    """豆包翻译器基础异常类"""
    pass

class DoubaoAuthenticationError(DoubaoError):
    """认证错误"""
    pass

class DoubaoConnectionError(DoubaoError):
    """连接错误"""
    pass

class DoubaoAPIError(DoubaoError):
    """API调用错误"""
    pass

class DoubaoConfigError(DoubaoError):
    """配置错误"""
    pass

class DoubaoValidationError(DoubaoError):
    """输入验证错误"""
    pass

# 性能配置常量
DEFAULT_PERFORMANCE_CONFIG = {
    'max_workers': 5,
    'cache_ttl': 3600,
    'min_request_interval': 0.1,
    'max_retries': 3,
    'timeout': 30,
    'temperature': 0.3,
    'max_tokens': 1024,
}

PERFORMANCE_PROFILES = {
    'fast': {
        'max_workers': 10,
        'cache_ttl': 1800,
        'min_request_interval': 0.05,
        'max_retries': 2,
        'timeout': 15,
        'temperature': 0.5,
        'max_tokens': 512,
    },
    'balanced': DEFAULT_PERFORMANCE_CONFIG,
    'accurate': {
        'max_workers': 3,
        'cache_ttl': 7200,
        'min_request_interval': 0.2,
        'max_retries': 5,
        'timeout': 60,
        'temperature': 0.1,
        'max_tokens': 2048,
    }
}

# 然后配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DoubaoTranslator')

# 设置langdetect的随机种子，确保结果一致性
DetectorFactory.seed = 0

# 从环境变量加载配置
ENV_CONFIG = {
    'API_KEY': None,
    'BASE_URL': None,
    'MODEL': None
}

try:
    # 尝试加载 .env 文件
    load_dotenv()
    
    # 读取配置项
    ENV_CONFIG['API_KEY'] = os.getenv('ARK_API_KEY')
    ENV_CONFIG['BASE_URL'] = os.getenv('ARK_BASE_URL', DEFAULT_BASE_URL)
    ENV_CONFIG['MODEL'] = os.getenv('ARK_MODEL', DEFAULT_MODEL)
    
    if ENV_CONFIG['API_KEY']:
        logger.info("Successfully loaded API key from environment")
    if ENV_CONFIG['BASE_URL'] != DEFAULT_BASE_URL:
        logger.info(f"Using custom base URL: {ENV_CONFIG['BASE_URL']}")
    if ENV_CONFIG['MODEL'] != DEFAULT_MODEL:
        logger.info(f"Using custom model: {ENV_CONFIG['MODEL']}")
        
except Exception as e:
    logger.warning(f"Error loading .env configuration: {str(e)}")

# 语言代码映射表
LANG_CODE_MAP = {
    # ISO 639-1 到豆包语言代码的映射
    'zh-cn': 'zh', 'zh-tw': 'zh', 'zh': 'zh',
    'en': 'en',
    'ja': 'ja',
    'ko': 'ko',
    'fr': 'fr',
    'es': 'es',
    'ru': 'ru',
    'de': 'de',
    'it': 'it',
    'tr': 'tr',
    'pt': 'pt',
    'vi': 'vi',
    'id': 'id',
    'th': 'th',
    'ms': 'ms',
    'ar': 'ar',
    'hi': 'hi'
}

class DoubaoTranslated:
    """表示豆包翻译结果的类"""
    def __init__(self, src, dest, origin, text, pronunciation=None):
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation

    def __repr__(self):
        return f'<DoubaoTranslated src={self.src} dest={self.dest} text={self.text} pronunciation={self.pronunciation}>'

class DoubaoDetected:
    """表示豆包语言检测结果的类"""
    def __init__(self, lang: str, confidence: float, details: Dict = None):
        self.lang = self._normalize_lang_code(lang)
        self.confidence = confidence
        self.details = details or {}

    def _normalize_lang_code(self, lang: str) -> str:
        """标准化语言代码"""
        return LANG_CODE_MAP.get(lang.lower(), lang.lower())

    def __repr__(self):
        if self.details:
            return f'<DoubaoDetected lang={self.lang} confidence={self.confidence:.3f} details={self.details}>'
        return f'<DoubaoDetected lang={self.lang} confidence={self.confidence:.3f}>'

class DoubaoTranslationError(Exception):
    """豆包翻译错误基类"""
    pass

class DoubaoAPIError(DoubaoTranslationError):
    """API错误"""
    pass

class DoubaoAuthenticationError(DoubaoTranslationError):
    """认证错误"""
    pass

class DoubaoConnectionError(DoubaoTranslationError):
    """连接错误"""
    pass

class PerformanceMetrics:
    """性能指标监控类"""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_latency = 0
        self.start_time = time.time()
        self._lock = threading.Lock()

    def record_request(self, latency: float, success: bool):
        """记录请求指标"""
        with self._lock:
            self.request_count += 1
            self.total_latency += latency
            if not success:
                self.error_count += 1

    def get_metrics(self) -> Dict[str, float]:
        """获取性能指标"""
        with self._lock:
            uptime = time.time() - self.start_time
            return {
                'request_count': self.request_count,
                'error_rate': self.error_count / max(self.request_count, 1),
                'avg_latency': self.total_latency / max(self.request_count, 1),
                'uptime': uptime,
                'requests_per_second': self.request_count / max(uptime, 1)
            }

    def reset(self):
        """重置指标"""
        with self._lock:
            self.request_count = 0
            self.error_count = 0
            self.total_latency = 0
            self.start_time = time.time()

class AsyncResourceManager:
    """异步资源管理器基类"""
    
    def __init__(self):
        self._initialized = False
        self._cleanup_lock = asyncio.Lock()
        self._init_lock = asyncio.Lock()

    async def initialize(self):
        """初始化资源"""
        if self._initialized:
            return
        async with self._init_lock:
            if not self._initialized:
                await self._do_initialize()
                self._initialized = True

    async def cleanup(self):
        """清理资源"""
        if not self._initialized:
            return
        async with self._cleanup_lock:
            if self._initialized:
                await self._do_cleanup()
                self._initialized = False

    async def _do_initialize(self):
        """实际的初始化逻辑"""
        raise NotImplementedError

    async def _do_cleanup(self):
        """实际的清理逻辑"""
        raise NotImplementedError

class SessionManager(AsyncResourceManager):
    """会话管理器"""
    
    def __init__(self):
        super().__init__()
        self.session = None
        self._session_lock = asyncio.Lock()

    async def _do_initialize(self):
        """初始化会话"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _do_cleanup(self):
        """清理会话"""
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None

    async def get_session(self):
        """获取会话，确保会话有效"""
        await self.initialize()
        async with self._session_lock:
            if self.session is None or self.session.closed:
                await self._do_initialize()
            return self.session

class ClientManager(AsyncResourceManager):
    """API客户端管理器"""
    
    def __init__(self, api_key: str, base_url: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.client = None
        self._client_lock = asyncio.Lock()

    async def _do_initialize(self):
        """初始化客户端"""
        if not self.client:
            self.client = openai.AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )

    async def _do_cleanup(self):
        """清理客户端"""
        if hasattr(self.client, 'close'):
            await self.client.close()
        self.client = None

    async def get_client(self):
        """获取客户端，确保客户端有效"""
        await self.initialize()
        async with self._client_lock:
            if not self.client:
                await self._do_initialize()
            return self.client

class BatchProcessor:
    """批处理器"""
    
    def __init__(self, max_workers: int, batch_size: int):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.queue = asyncio.Queue()
        self.results = []
        self.tasks = set()
        self.semaphore = asyncio.Semaphore(max_workers)
        self._stop_event = asyncio.Event()

    async def process(self, items: List[Any], processor_func) -> List[Any]:
        """处理项目列表
        
        Args:
            items: 要处理的项目列表
            processor_func: 处理单个项目的异步函数
        """
        self.results = [None] * len(items)
        workers = [self._worker(processor_func) for _ in range(self.max_workers)]

        # 填充队列
        for i, item in enumerate(items):
            await self.queue.put((i, item))

        # 添加结束标记
        for _ in range(self.max_workers):
            await self.queue.put((None, None))

        # 等待所有工作完成
        await asyncio.gather(*workers)
        return self.results

    async def _worker(self, processor_func):
        """工作协程"""
        while not self._stop_event.is_set():
            try:
                index, item = await self.queue.get()
                if index is None:  # 结束标记
                    self.queue.task_done()
                    break

                try:
                    async with self.semaphore:
                        result = await processor_func(item)
                        self.results[index] = result
                except Exception as e:
                    logger.error(f"Error processing item at index {index}: {e}")
                    self.results[index] = None
                finally:
                    self.queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
                continue

    async def stop(self):
        """停止处理"""
        self._stop_event.set()
        while not self.queue.empty():
            try:
                await self.queue.get()
                self.queue.task_done()
            except:
                pass

class AsyncCache:
    """异步安全的缓存实现"""
    
    def __init__(self, ttl: int = 3600):
        self._cache = {}
        self._ttl = ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        async with self._lock:
            if key in self._cache:
                item = self._cache[key]
                if time.time() - item['timestamp'] < self._ttl:
                    return item['value']
                else:
                    del self._cache[key]
        return None

    async def set(self, key: str, value: Any) -> None:
        """设置缓存项"""
        async with self._lock:
            self._cache[key] = {
                'value': value,
                'timestamp': time.time()
            }
            await self._cleanup()

    async def _cleanup(self) -> None:
        """清理过期缓存"""
        current_time = time.time()
        async with self._lock:
            expired = [
                k for k, v in self._cache.items()
                if current_time - v['timestamp'] > self._ttl
            ]
            for k in expired:
                del self._cache[k]

    async def clear(self) -> None:
        """清空缓存"""
        async with self._lock:
            self._cache.clear()

class DoubaoTranslator:
    """豆包AI翻译器类"""

    def __init__(self, api_key=None, model_name=None, base_url=None, 
                 max_workers=MAX_WORKERS, glossary_path=None,
                 performance_mode='balanced', **kwargs):
        """
        初始化DoubaoTranslator对象。

        Args:
            api_key: 豆包API密钥，如未提供则从环境变量获取
            model_name: 豆包模型名称，如未提供则使用默认模型
            base_url: 豆包API的基础URL，如未提供则使用默认URL
            max_workers: 最大并发线程数
            glossary_path: 术语表文件路径
            performance_mode: 性能模式('fast', 'balanced', 'accurate')
            **kwargs: 自定义性能参数，可覆盖预设配置

        Raises:
            DoubaoConfigError: 配置参数无效
            DoubaoAuthenticationError: API密钥无效
            DoubaoValidationError: 参数验证失败
        """
        try:
            # 确保环境变量已加载
            load_dotenv()
            
            # 验证并设置API密钥
            self.api_key = api_key or os.getenv('ARK_API_KEY')
            if not self.api_key:
                raise DoubaoAuthenticationError("API密钥未提供。请通过参数传入api_key或设置环境变量 ARK_API_KEY")
            
            if not isinstance(self.api_key, str) or len(self.api_key) < 32:
                raise DoubaoAuthenticationError("API密钥格式无效")
                
            # 设置基础配置
            self.base_url = base_url or os.getenv('ARK_BASE_URL', DEFAULT_BASE_URL)
            self.model = model_name or os.getenv('ARK_MODEL', DEFAULT_MODEL)
            
            # 验证性能模式
            if performance_mode not in PERFORMANCE_PROFILES:
                raise DoubaoConfigError(f"无效的性能模式。必须是: {', '.join(PERFORMANCE_PROFILES.keys())}")
            
            # 加载性能配置
            self.perf_config = PERFORMANCE_PROFILES[performance_mode].copy()
            self.perf_config.update(kwargs)  # 允许通过kwargs覆盖特定配置
            
            # 验证配置参数
            self._validate_config(self.perf_config)
            
            # 应用性能配置
            self._cache_ttl = self.perf_config['cache_ttl']
            self._min_request_interval = self.perf_config['min_request_interval']
            self.max_retries = self.perf_config['max_retries']
            
            # 初始化资源管理器
            self.session_manager = SessionManager()
            self.client_manager = ClientManager(self.api_key, self.base_url)
            self.semaphore = asyncio.Semaphore(self.perf_config['max_workers'])
            
            # 初始化异步锁
            self._cache_lock = asyncio.Lock()
            self._request_lock = asyncio.Lock()
            self._metrics_lock = asyncio.Lock()
            
            # 初始化其他组件
            self._init_components(max_workers, glossary_path)
            
            logger.info(f"DoubaoTranslator initialized with model: {self.model} and performance_mode: {performance_mode}")
            
        except Exception as e:
            logger.error(f"Initialization failed: {str(e)}")
            raise

    def _init_components(self, max_workers: int, glossary_path: Optional[str]):
        """初始化组件

        Args:
            max_workers: 最大并发数
            glossary_path: 术语表路径
        """
        # 基础组件
        self._last_request_time = 0
        self._response_cache = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.system_prompt = "你是豆包翻译助手，请直接翻译用户的文本，不要添加任何解释。"
        
        # 术语表初始化
        self.glossary: Dict[str, Dict[str, str]] = {}
        if glossary_path:
            self.load_glossary(glossary_path)
        
        # 风格模板初始化
        self._init_style_templates()
        
        # 性能监控
        self.metrics = PerformanceMetrics()
        
        # 异步组件
        self.session = None
        self.semaphore = asyncio.Semaphore(max_workers)

    def _init_style_templates(self):
        """初始化翻译风格模板"""
        self.style_templates = {
            'formal': """
                翻译要求：
                1. 使用正式的学术用语
                2. 保持严谨的句式结构
                3. 使用标准的专业术语
                4. 避免口语化和简化表达
            """,
            'casual': """
                翻译要求：
                1. 使用日常口语表达
                2. 保持语言自然流畅
                3. 使用简短句式
                4. 可以使用常见缩写
            """,
            'technical': """
                翻译要求：
                1. 严格使用技术术语
                2. 保持专业准确性
                3. 使用规范的技术表达
                4. 保持术语一致性
            """,
            'creative': """
                翻译要求：
                1. 提供2-3个不同的翻译版本
                2. 每个版本使用不同的表达方式
                3. 保持原文的核心含义
                4. 限制在3个版本以内
            """
        }

    def _should_retry(self, exception: Exception) -> bool:
        """判断是否应该重试"""
        if isinstance(exception, (openai.APIError, openai.APIConnectionError)):
            return True
        if isinstance(exception, httpx.ConnectError):
            return True
        return False

    def _get_retry_config(self):
        """获取重试配置"""
        return {
            'multiplier': self.perf_config.get('retry_multiplier', 0.5),
            'min': self.perf_config.get('retry_min_wait', 1),
            'max': self.perf_config.get('retry_max_wait', 4),
            'max_retries': self.perf_config.get('max_retries', 3)
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=1, max=4),
        retry=retry_if_exception_type((openai.APIError, openai.APIConnectionError, httpx.ConnectError))
    )
    async def _make_request(self, messages, stream=False):
        """改进的异步请求处理"""
        async with self._request_lock:  # 使用请求锁控制并发
            current_time = time.time()
            time_since_last_request = current_time - self._last_request_time
            if time_since_last_request < self._min_request_interval:
                await asyncio.sleep(self._min_request_interval - time_since_last_request)
            
            start_time = time.time()
            request_id = str(uuid.uuid4())
            
            try:
                # 验证API密钥
                if not self.api_key or len(self.api_key) < 32:
                    raise DoubaoAuthenticationError("无效的API密钥")

                client = await self.client_manager.get_client()
                
                async with self.semaphore:  # 使用信号量控制并发
                    try:
                        completion = await client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            stream=stream,
                            temperature=self.perf_config['temperature'],
                            max_tokens=self.perf_config['max_tokens'],
                            timeout=self.perf_config['timeout']
                        )
                    except openai.AuthenticationError as e:
                        raise DoubaoAuthenticationError(f"API认证失败: {str(e)}")
                    except openai.APIError as e:
                        if "auth" in str(e).lower():
                            raise DoubaoAuthenticationError(f"API认证失败: {str(e)}")
                        raise
                    
                    self._last_request_time = time.time()
                    duration = time.time() - start_time
                    
                    if stream:
                        return completion
                    else:
                        if hasattr(completion, 'choices') and completion.choices:
                            result = completion.choices[0].message.content.strip()
                            await self._record_metrics(duration, True)
                            return result
                        else:
                            raise DoubaoAPIError("Invalid API response format")
                
            except openai.AuthenticationError as e:
                await self._record_metrics(time.time() - start_time, False)
                raise DoubaoAuthenticationError(f"认证失败: {str(e)}")
            except openai.APIConnectionError as e:
                await self._record_metrics(time.time() - start_time, False)
                raise DoubaoConnectionError(f"连接失败: {str(e)}")
            except asyncio.TimeoutError:
                await self._record_metrics(time.time() - start_time, False)
                raise DoubaoAPIError("请求超时")
            except Exception as e:
                await self._record_metrics(time.time() - start_time, False)
                logger.error(f"Request {request_id} failed after {time.time() - start_time:.2f}s: {str(e)}")
                raise DoubaoAPIError(f"API请求失败: {str(e)}")

    async def _record_metrics(self, duration: float, success: bool) -> None:
        """异步安全的指标记录"""
        async with self._metrics_lock:
            self.metrics.record_request(duration, success)

    def _get_cache_key(self, messages):
        """生成缓存键"""
        # 只使用消息内容和角色生成缓存键
        key_parts = [f"{m['role']}:{m['content']}" for m in messages]
        return hash(tuple(key_parts))

    def _get_from_cache(self, key):
        """从缓存获取响应"""
        if key in self._response_cache:
            cached_item = self._response_cache[key]
            if time.time() - cached_item['timestamp'] < self._cache_ttl:
                return cached_item['response']
            else:
                del self._response_cache[key]
        return None

    def _add_to_cache(self, key, response):
        """添加响应到缓存"""
        self._response_cache[key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        # 清理过期缓存
        self._cleanup_cache()

    def _cleanup_cache(self):
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = [
            k for k, v in self._response_cache.items()
            if current_time - v['timestamp'] > self._cache_ttl
        ]
        for k in expired_keys:
            del self._response_cache[k]

    async def _init_session(self):
        """初始化异步会话"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def _close_session(self):
        """关闭异步会话"""
        if self.session:
            await self.session.close()
            self.session = None

    async def translate_batch(self, texts: List[str], dest='en', src='auto', batch_size=10) -> List[DoubaoTranslated]:
        """异步批量翻译

        Args:
            texts: 要翻译的文本列表
            dest: 目标语言代码
            src: 源语言代码（auto为自动检测）
            batch_size: 每批处理的文本数量

        Returns:
            翻译结果列表
        """
        if not texts:
            return []

        start_time = time.time()
        processor = BatchProcessor(
            max_workers=self.perf_config['max_workers'],
            batch_size=batch_size
        )

        async def translate_single(text: str) -> DoubaoTranslated:
            try:
                return await self._doubao_translate_single(text, dest, src, False)
            except Exception as e:
                logger.error(f"Translation failed: {text[:50]}... Error: {str(e)}")
                return DoubaoTranslated(
                    src=src,
                    dest=dest,
                    origin=text,
                    text=f"Translation failed: {str(e)}"
                )

        try:
            results = await processor.process(texts, translate_single)
            
            duration = time.time() - start_time
            success_count = sum(1 for r in results if r and not r.text.startswith("Translation failed"))
            logger.info(f"Batch translation completed in {duration:.2f}s - {len(texts)} texts, {success_count} successful")
            
            return results
        finally:
            await processor.stop()

    def translate_batch_sync(self, texts: List[str], dest='en', src='auto') -> List[DoubaoTranslated]:
        """同步批量翻译实现

        Args:
            texts: 要翻译的文本列表
            dest: 目标语言代码
            src: 源语言代码（auto为自动检测）

        Returns:
            翻译结果列表
        """
        try:
            return asyncio.run(self.translate_batch(texts, dest, src))
        except Exception as e:
            logger.error(f"Sync batch translation failed: {str(e)}")
            return [DoubaoTranslated(src, dest, text, f"Translation failed: {str(e)}") for text in texts]

    def load_glossary(self, path: Union[str, Path]) -> None:
        """
        加载术语表

        :param path: 术语表文件路径
        :raises: FileNotFoundError 如果文件不存在
        :raises: json.JSONDecodeError 如果JSON格式无效
        """
        try:
            path = Path(path)
            if not path.exists():
                raise FileNotFoundError(f"术语表文件不存在: {path}")
            
            with path.open('r', encoding='utf-8') as f:
                self.glossary = json.load(f)
            
            logger.info(f"Loaded glossary with {len(self.glossary)} terms from {path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in glossary file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading glossary: {e}")
            raise

    def save_glossary(self, path: Union[str, Path]) -> None:
        """
        保存术语表

        :param path: 保存路径
        """
        try:
            path = Path(path)
            with path.open('w', encoding='utf-8') as f:
                json.dump(self.glossary, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved glossary to {path}")
        except Exception as e:
            logger.error(f"Error saving glossary: {e}")
            raise

    def add_term(self, term_id: str, translations: Dict[str, str]) -> None:
        """
        加或更新术语

        :param term_id: 术语ID
        :param translations: 各语言的翻译
        """
        self.glossary[term_id] = translations
        logger.debug(f"Added/updated term: {term_id} with translations: {translations}")

    async def apply_glossary(self, text: str, src: str, dest: str) -> DoubaoTranslated:
        """应用术语表进行翻译"""
        if not self.glossary:
            return await self.doubao_translate(text, dest=dest, src=src)

        try:
            # 创建术语替换映射
            replacements = {}
            placeholder_format = "[[TERM_{}_]]"
            
            # 第一步：替换术语为占位符
            modified_text = text
            for term_id, translations in self.glossary.items():
                if src in translations and dest in translations:
                    source_term = translations[src]
                    target_term = translations[dest]
                    
                    # 使用正则表达式进行完整词匹配
                    pattern = r'\b' + re.escape(source_term) + r'\b'
                    if re.search(pattern, modified_text, re.IGNORECASE):
                        placeholder = placeholder_format.format(term_id)
                        modified_text = re.sub(
                            pattern,
                            placeholder,
                            modified_text,
                            flags=re.IGNORECASE
                        )
                        replacements[placeholder] = target_term

            # 如果没有找到任何术语匹配，直接翻译原文
            if not replacements:
                return await self.doubao_translate(text, dest=dest, src=src)

            # 第二步：翻译修改后的文本
            translated = await self.doubao_translate(modified_text, dest=dest, src=src)
            result = translated.text

            # 第三步：还原术语
            for placeholder, term in replacements.items():
                result = result.replace(placeholder, term)

            logger.debug(f"Applied glossary translation with {len(replacements)} terms")
            return DoubaoTranslated(src, dest, text, result)

        except Exception as e:
            logger.error(f"Error applying glossary: {e}")
            # 如果术语表应用失败，回退到普通翻译
            return await self.doubao_translate(text, dest=dest, src=src)

    def get_term(self, term_id: str) -> Optional[Dict[str, str]]:
        """
        获取术语的翻译

        :param term_id: 术语ID
        :return: 术语的翻译字典，如果不存在返回None
        """
        return self.glossary.get(term_id)

    async def _doubao_translate_single(self, text: str, dest: str, src: str, stream: bool):
        """单个文本翻译实现"""
        try:
            text = text.strip()
            if not text:
                return DoubaoTranslated(src, dest, text, text)

            # 对于流式翻译，不使用缓存
            if not stream:
                cache_key = f"{text}:{src}:{dest}"
                cached_result = self._get_from_cache(cache_key)
                if cached_result:
                    return cached_result

            if src == 'auto':
                try:
                    detected = await self.doubao_detect(text)
                    src = detected.lang
                except Exception as e:
                    logger.warning(f"Language detection failed, using 'auto': {str(e)}")

            prompt = f"将以下{src}文本翻译成{dest}：\n{text}"
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            start_time = time.time()
            translated_text = await self._make_request(messages, stream=False)
            duration = time.time() - start_time
            self.metrics.record_request(duration, True)

            result = DoubaoTranslated(
                src=src,
                dest=dest,
                origin=text,
                text=translated_text.strip()
            )

            # 只缓存非流式翻译结果
            if not stream:
                self._add_to_cache(cache_key, result)
            return result

        except Exception as e:
            logger.error(f"Translation failed for text: {text[:50]}... Error: {str(e)}")
            raise DoubaoAPIError(f"翻译失败: {str(e)}")

    async def doubao_translate(self, text: Union[str, List[str]], dest='en', src='auto', stream=False) -> Union[DoubaoTranslated, List[DoubaoTranslated]]:
        """
        翻译文本，支持批量处理和流式翻译

        Args:
            text: 要翻译的源文本（字符串或字符串列表）
            dest: 目标语言
            src: 源语言
            stream: 是否使用流式翻译

        Returns:
            翻译结果或生成器（流式翻译时）
        """
        # 验证语言代码
        if src != 'auto' and src not in DOUBAO_LANGUAGES:
            raise DoubaoError(f"不支持的源语言: {src}")
        if dest not in DOUBAO_LANGUAGES:
            raise DoubaoError(f"不支持的目标语言: {dest}")

        if isinstance(text, list):
            if stream:
                raise ValueError("流式翻译不支持批量处理")
            result = await self.translate_batch(text, dest, src)
            return result
        
        if not stream:
            result = await self._doubao_translate_single(text, dest, src, False)
            return result
            
        # 流式翻译逻辑
        async def stream_translate():
            text_to_translate = text.strip()
            if not text_to_translate:
                yield DoubaoTranslated(src, dest, text_to_translate, text_to_translate)
                return

            current_src = src
            if current_src == 'auto':
                try:
                    detected = await self.doubao_detect(text_to_translate)
                    current_src = detected.lang
                except Exception as e:
                    logger.warning(f"Language detection failed, using 'auto': {str(e)}")

            prompt = f"将以下{current_src}文本翻译成{dest}：\n{text_to_translate}"
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            try:
                response_stream = await self._make_request(messages, stream=True)
                translated_text = ""
                async for chunk in response_stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        translated_text += chunk.choices[0].delta.content
                        yield DoubaoTranslated(current_src, dest, text_to_translate, translated_text)
            except Exception as e:
                logger.error(f"Streaming translation failed: {str(e)}")
                raise DoubaoAPIError(f"流式翻译失败: {str(e)}")
        
        return stream_translate()

    def _normalize_detection_result(self, detected_text: str) -> str:
        """规范化语言检测结果"""
        # 处理直接返回语言代码的情况
        if len(detected_text) <= 3:
            return detected_text.lower()
        
        # 处理返回描述文本的情况
        lang_patterns = {
            r'.*韩语.*': 'ko',
            r'.*法语.*': 'fr',
            r'.*中文.*': 'zh',
            r'.*英语.*': 'en',
            r'.*日语.*': 'ja',
            r'.*俄语.*': 'ru',
            r'.*德语.*': 'de',
            r'.*阿拉伯语.*': 'ar'
        }
        
        for pattern, code in lang_patterns.items():
            if re.search(pattern, detected_text):
                return code
        
        return detected_text.lower()

    @retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def doubao_detect(self, text: str) -> DoubaoDetected:
        """
        检测文本语言

        :param text: 要检测语言的文本
        :return: DoubaoDetected对象
        """
        try:
            messages = [
                {"role": "system", "content": "你是豆包语言检测助手，请只返回检测到的语言代码，例如：en、zh、ja等"},
                {"role": "user", "content": f"检测下面文本的语言：\n{text}"}
            ]

            response = await self._make_request(messages)
            # 直接使用返回的字符串，因为_make_request已经处理了response.choices[0].message.content
            detected_lang = self._normalize_detection_result(response)
            return DoubaoDetected(detected_lang, 1.0)

        except Exception as e:
            logger.error(f"Language detection failed for text: {text[:50]}... Error: {str(e)}")
            raise

    async def _cached_detect(self, text: str) -> Tuple[str, float]:
        """缓存的语言检测"""
        cache_key = f"detect_{text[:100]}"  # 使用前100个字符作为键
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result.lang, cached_result.confidence
            
        result = await self.doubao_detect(text)
        self._add_to_cache(cache_key, result)
        return result.lang, result.confidence

    async def doubao_detect_enhanced(self, text: str) -> DoubaoDetected:
        """
        增强的语言检测功能，结合多个检测器的结果

        Args:
            text: 要检测语言的文本
        Returns:
            DoubaoDetected对象，包含检测结果和置信度
        """
        try:
            # 初始化结果字典
            lang_scores: Dict[str, float] = {}
            
            # 1. 使用豆包API检测
            try:
                doubao_lang, doubao_confidence = await self._cached_detect(text)
                lang_scores[doubao_lang] = doubao_confidence * 1.2  # 给豆包结果更高权重
                logger.debug(f"Doubao detection: {doubao_lang} ({doubao_confidence})")
            except Exception as e:
                logger.warning(f"Doubao detection failed: {str(e)}")

            # 2. 使用langdetect检测
            try:
                langdetect_results = detect_langs(text)
                for result in langdetect_results:
                    normalized_lang = LANG_CODE_MAP.get(result.lang, result.lang)
                    current_score = lang_scores.get(normalized_lang, 0)
                    lang_scores[normalized_lang] = current_score + result.prob
                    logger.debug(f"Langdetect detection: {normalized_lang} ({result.prob})")
            except LangDetectException as e:
                logger.warning(f"Langdetect detection failed: {str(e)}")

            # 3. 如果没有得到任何结果
            if not lang_scores:
                raise ValueError("No language detection results available")

            # 4. 找出得分最高的语言
            best_lang, best_score = max(lang_scores.items(), key=lambda x: x[1])
            
            # 5. 计算置信度得分（归一化到0-1范围）
            total_score = sum(lang_scores.values())
            confidence = best_score / total_score if total_score > 0 else 0

            # 6. 返回增强的语言检测结果
            return DoubaoDetected(
                lang=best_lang,
                confidence=confidence,
                details={
                    'raw_scores': lang_scores,
                    'detection_methods': {
                        'doubao': bool('doubao_lang' in locals()),
                        'langdetect': bool('langdetect_results' in locals())
                    }
                }
            )

        except Exception as e:
            logger.error(f"Enhanced language detection failed: {str(e)}")
            raise Exception(f"语言检测失败: {str(e)}")

    def get_supported_languages(self) -> List[str]:
        """
        获取支持的语言列表

        :return: 支持的语言代码列表
        """
        return list(DOUBAO_LANGUAGES.keys())

    def is_language_supported(self, lang_code: str) -> bool:
        """
        检查语言是否被支持

        :param lang_code: 语言代码
        :return: 是否支持该语言
        """
        normalized_code = LANG_CODE_MAP.get(lang_code.lower(), lang_code.lower())
        return normalized_code in DOUBAO_LANGUAGES

    def __del__(self):
        """确保资源正确释放"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)
        if hasattr(self, 'session') and self.session:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self._close_session())
            else:
                try:
                    loop.run_until_complete(self._close_session())
                except Exception:
                    pass  # 忽略关闭时的错误

    async def translate_with_context(self, text: str, context: str, dest='en', src='auto', style_guide=None) -> DoubaoTranslated:
        """
        带上下文的翻译，支持风格指南和一致性控制

        Args:
            text: 要翻译的文本
            context: 上下文信息
            dest: 目标语言
            src: 源语言（auto为自动检测）
            style_guide: 风格指南（可选）

        Returns:
            DoubaoTranslated对象
        """
        try:
            # 1. 如果语言auto，先进行语言检测
            if src == 'auto':
                try:
                    detected = await self.doubao_detect(text)
                    src = detected.lang
                    logger.debug(f"Detected source language: {src}")
                except Exception as e:
                    logger.warning(f"Language detection failed, using 'auto': {str(e)}")

            # 2. 构建提示词
            style_instructions = ""
            if style_guide:
                style_instructions = f"\n\n风格要求：\n{style_guide}"

            prompt = f"""请在理解以下上下文的基础上，将文本从{src}翻译成{dest}：

上下文背景：
{context}

需要翻译的文本：
{text}

翻译要求：
1. 保持与上下文的连贯性和一致性
2. 保留专业术语准确性
3. 保持原文的语气和风格
4. 保持代词指代的正确性
5. 注意上下文中的特定含义{style_instructions}

请直接返回翻译结果，不要添加任何解释。"""

            # 3. 应用术语表（如果有）
            if self.glossary:
                try:
                    logger.debug("Applying glossary before context translation")
                    glossary_result = await self.apply_glossary(text, src, dest)
                    text = glossary_result.text
                except Exception as e:
                    logger.warning(f"Glossary application failed: {str(e)}")

            # 4. 发送翻译请求
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]

            translated_text = await self._make_request(messages, stream=False)

            # 5. 记录翻译结果
            logger.info(f"Context-aware translation completed for text length: {len(text)}")
            logger.debug(f"Translation context length: {len(context)}")

            return DoubaoTranslated(
                src=src,
                dest=dest,
                origin=text,
                text=translated_text
            )

        except Exception as e:
            logger.error(f"Context-aware translation failed: {str(e)}")
            raise Exception(f"上下文感知翻译失败: {str(e)}")

    async def translate_document_with_context(self, 
                                           paragraphs: List[str], 
                                           dest='en', 
                                           src: str = 'auto', 
                                           context_window: int = 2,
                                           batch_size: int = 5,
                                           style_guide: str = None) -> List[DoubaoTranslated]:
        """
        翻译整个文档，使用滑动窗口保持上下文连贯性

        Args:
            paragraphs: 段落列表
            dest: 目标语言
            src: 源语言
            context_window: 上下文窗口大小（前后考虑几个段落）
            batch_size: 批处理大小
            style_guide: 风格指南

        Returns:
            翻译结果列表
        """
        translator = DocumentTranslator(
            translator=self,
            context_window=context_window,
            batch_size=batch_size
        )
        return await translator.translate_document(
            paragraphs=paragraphs,
            dest=dest,
            src=src,
            style_guide=style_guide
        )

    def add_style_template(self, name: str, template: str) -> None:
        """
        添加新的风格模板

        :param name: 模板名称
        :param template: 模板内容
        """
        self.style_templates[name] = template
        logger.info(f"Added new style template: {name}")

    def get_style_template(self, name: str) -> str:
        """
        获取风格模板

        :param name: 模板名称
        :return: 模板内容
        """
        return self.style_templates.get(name)

    def _format_creative_translation(self, text: str) -> str:
        """格式化创意翻译结果"""
        # 取实际的翻译内容
        translations = []
        for line in text.split('\n'):
            # 移除版本标记、序号等
            line = line.strip()
            if not line or line.startswith('版本') or line.startswith('以下') or line == '-':
                continue
            # 移除序号和折号
            line = re.sub(r'^[-\d\.\s]+', '', line.strip())
            if line:
                translations.append(line)
        
        # 限制版本数量并用分号连接
        return ' ; '.join(translations[:3])

    def _format_translation_result(self, text: str, style: str) -> str:
        """格式化翻译结果"""
        if style == 'creative':
            return self._format_creative_translation(text)
        return text.strip()

    def validate_style(self, style: Union[str, Dict[str, str]]) -> Tuple[bool, str]:
        """
        验证翻译风格的有效性

        :param style: 风格名称或自定义风格配置
        :return: (是否有效, 建议或错误信息)
        """
        if isinstance(style, str):
            if style in self.style_templates:
                return True, "风格有效"
            return False, f"未知的风格名称。可用风格: {', '.join(self.style_templates.keys())}"
        
        if isinstance(style, dict):
            required_keys = {'语气', '表达方式', '专业程度'}
            missing_keys = required_keys - set(style.keys())
            if missing_keys:
                return False, f"自定义风格缺少必要的配置项: {', '.join(missing_keys)}"
            return True, "自定义风格配置有效"
        
        return False, "风格必须是预定义名称或配置字典"

    async def translate_with_style(self, text: str, dest: str = 'en', src: str = 'auto', 
                            style: Union[str, Dict] = 'formal', context: str = None,
                            max_versions: int = 3) -> DoubaoTranslated:
        """
        带风格的翻译

        :param text: 要翻译的文本
        :param dest: 目标语言
        :param src: 源语言
        :param style: 翻译风格，可以是预定义风格的名称或自定义风格字典
        :param context: 上下文信息
        :param max_versions: 创意风格时的最大版本数量，默认3个
        :return: DoubaoTranslated对象
        """
        start_time = time.time()
        try:
            # 构建提示信息
            if isinstance(style, str):
                if style not in self.style_templates:
                    raise ValueError(f"未知的预定义风格: {style}")
                style_prompt = self.style_templates[style]
                if style == 'creative':
                    # 动态更新创意风格的版本数限制
                    style_prompt = f"""
                    翻译要求：
                    1. 提供{max_versions}个不同的翻译版本
                    2. 每个版本使用不同的表达方式
                    3. 保持原文的核心含义
                    4. 限制在{max_versions}个版本以内
                    """
            else:
                # 将自定义风格字典转换为提示文本
                style_prompt = "翻译要求：\n" + "\n".join([f"{k}: {v}" for k, v in style.items()])

            # 添加上下文信息（如果有）
            context_part = f"\n相关上下文：\n{context}\n" if context else ""

            messages = [
                {"role": "system", "content": "你是一个专业的翻译手，请按照指定的风格要求进行翻译。"},
                {"role": "user", "content": f"""
{style_prompt}

{context_part}
需要翻译的文本：
{text}

请直接提供翻译结果，不要添加任何解释。如果是创意风格，最多提供{max_versions}个不同的版本，用分号分隔。
"""}
            ]

            response = await self._make_request(messages, stream=False)
            translated_text = response.choices[0].message.content.strip()

            duration = time.time() - start_time
            logger.info(f"Styled translation completed in {duration:.2f}s - Style: {style}, Length: {len(text)}, Languages: {src}->{dest}")

            return DoubaoTranslated(
                src=src,
                dest=dest,
                origin=text,
                text=translated_text
            )

        except Exception as e:
            logger.error(f"Style translation failed: {str(e)}")
            raise Exception(f"风格化翻译失败: {str(e)}")

    async def evaluate_translation(self, original: str, translated: str, src: str, dest: str) -> Dict[str, float]:
        """
        评估翻译质量
        
        :return: 包含各项指标的字典
        """
        prompt = f"""请评估以下翻译的质量，给出0-1的分数：

原文 ({src}): {original}
译文 ({dest}): {translated}

请从以下几个方面评分：
1. 准确性：内容是否准确传达
2. 流畅性：是否自流畅
3. 专业性：专业术语使用是否恰当
4. 风格：是否保持原文风格

只返回JSON式的评分结果。"""

        try:
            messages = [
                {"role": "system", "content": "你是翻译质量评估专家"},
                {"role": "user", "content": prompt}
            ]
            
            response = await self._make_request(messages)
            scores = json.loads(response.choices[0].message.content)
            return scores

        except Exception as e:
            logger.error(f"Translation evaluation failed: {str(e)}")
            return {
                "accuracy": 0.0,
                "fluency": 0.0,
                "professionalism": 0.0,
                "style": 0.0
            }

    @lru_cache(maxsize=1000)
    def _get_cached_translation(self, text: str, dest: str, src: str, style: str = None) -> str:
        """获取缓存的翻译结果"""
        cache_key = f"{text}:{src}:{dest}:{style}"
        return cache_key

    def set_performance_config(self, **kwargs):
        """
        动态更新性能配置

        :param kwargs: 要更新的性能参数
        """
        self.perf_config.update(kwargs)
        # 更新相关实例变量
        if 'cache_ttl' in kwargs:
            self._cache_ttl = kwargs['cache_ttl']
        if 'min_request_interval' in kwargs:
            self._min_request_interval = kwargs['min_request_interval']
        if 'max_retries' in kwargs:
            self.max_retries = kwargs['max_retries']

    async def test_connection(self) -> bool:
        """测试API连接和认证"""
        try:
            response = await self._make_request([
                {"role": "system", "content": "test"},
                {"role": "user", "content": "test"}
            ])
            logger.info("API连接测试成功")
            return True
        except Exception as e:
            logger.error(f"API连接测试失败: {str(e)}")
            return False

    def get_config(self) -> dict:
        """
        获取当前配置信息

        :return: 包含所有配置信息的字典
        """
        return {
            'api_key': f"{self.api_key[:8]}...",  # 只显示前8位
            'base_url': self.base_url,
            'model': self.model,
            'performance_config': self.perf_config,
            'cache_ttl': self._cache_ttl,
            'min_request_interval': self._min_request_interval,
            'max_retries': self.max_retries
        }

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """验证配置参数"""
        required_fields = {
            'max_retries': (int, lambda x: x > 0),
            'cache_ttl': (int, lambda x: x > 0),
            'max_tokens': (int, lambda x: 0 < x <= 2048),
            'temperature': (float, lambda x: 0 <= x <= 1),
        }
        
        for field, (field_type, validator) in required_fields.items():
            value = config.get(field)
            if not isinstance(value, field_type):
                raise ValueError(f"{field} must be of type {field_type.__name__}")
            if not validator(value):
                raise ValueError(f"Invalid value for {field}: {value}")

    async def __aenter__(self):
        """异步上下文管理器入口"""
        try:
            await self.session_manager.initialize()
            await self.client_manager.initialize()
            return self
        except Exception as e:
            logger.error(f"Failed to initialize resources: {e}")
            await self.__aexit__(type(e), e, e.__traceback__)
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        try:
            await self.session_manager.cleanup()
            await self.client_manager.cleanup()
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=False)
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            if exc_type is None:
                raise

    async def _ensure_session(self):
        """确保会话已初始化"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _cleanup_resources(self):
        """清理所有资源"""
        try:
            if hasattr(self, 'client'):
                await self.client.close()
            
            if hasattr(self, 'session') and self.session:
                if not self.session.closed:
                    await self.session.close()
                self.session = None
            
            if hasattr(self, 'executor'):
                self.executor.shutdown(wait=False)
            
            # 清理缓存
            self._response_cache.clear()
            
            logger.debug("Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during resource cleanup: {str(e)}")

# 豆包支持的语言代码常量
DOUBAO_LANGUAGES = {
    'zh': 'chinese',
    'en': 'english',
    'ja': 'japanese',
    'ko': 'korean',
    'fr': 'french',
    'es': 'spanish',
    'ru': 'russian',
    'de': 'german',
    'it': 'italian',
    'tr': 'turkish',
    'pt': 'portuguese',
    'vi': 'vietnamese',
    'id': 'indonesian',
    'th': 'thai',
    'ms': 'malay',
    'ar': 'arabic',
    'hi': 'hindi'
}

class DocumentTranslator:
    """文档翻译器"""
    
    def __init__(self, translator: 'DoubaoTranslator', context_window: int = 2, batch_size: int = 5):
        self.translator = translator
        self.context_window = context_window
        self.batch_size = batch_size
        self.processor = BatchProcessor(
            max_workers=translator.perf_config['max_workers'],
            batch_size=batch_size
        )
        self._paragraphs = []
        self._context_cache = {}

    def _get_context(self, index: int) -> str:
        """获取指定段落的上下文"""
        if index in self._context_cache:
            return self._context_cache[index]
            
        start_idx = max(0, index - self.context_window)
        end_idx = min(len(self._paragraphs), index + self.context_window + 1)
        context_paras = self._paragraphs[start_idx:index] + self._paragraphs[index+1:end_idx]
        context = "\n".join(context_paras)
        
        self._context_cache[index] = context
        return context

    async def translate_document(self, 
                               paragraphs: List[str], 
                               dest: str = 'en', 
                               src: str = 'auto',
                               style_guide: str = None) -> List[DoubaoTranslated]:
        """翻译整个文档
        
        Args:
            paragraphs: 段落列表
            dest: 目标语言
            src: 源语言
            style_guide: 风格指南
        """
        if not paragraphs:
            return []

        self._paragraphs = paragraphs
        self._context_cache.clear()
        start_time = time.time()

        async def translate_paragraph(text: str, index: int) -> DoubaoTranslated:
            try:
                context = self._get_context(index)
                return await self.translator.translate_with_context(
                    text=text,
                    context=context,
                    dest=dest,
                    src=src,
                    style_guide=style_guide
                )
            except Exception as e:
                logger.error(f"Failed to translate paragraph {index}: {str(e)}")
                return DoubaoTranslated(
                    src=src,
                    dest=dest,
                    origin=text,
                    text=f"Translation failed: {str(e)}"
                )

        try:
            # 创建任务列表
            tasks = []
            for i, text in enumerate(paragraphs):
                tasks.append(translate_paragraph(text, i))

            # 分批执行任务
            results = []
            for i in range(0, len(tasks), self.batch_size):
                batch = tasks[i:i + self.batch_size]
                batch_results = await asyncio.gather(*batch)
                results.extend(batch_results)

            duration = time.time() - start_time
            success_count = sum(1 for r in results if not r.text.startswith("Translation failed"))
            logger.info(
                f"Document translation completed in {duration:.2f}s - "
                f"{len(paragraphs)} paragraphs, {success_count} successful"
            )

            return results
        finally:
            self._context_cache.clear()
            self._paragraphs = []

class StreamTranslator:
    """流式翻译迭代器"""
    
    def __init__(self, translator, text: str, dest: str, src: str):
        self.translator = translator
        self.text = text
        self.dest = dest
        self.src = src

    async def __aiter__(self):
        """实现异步迭代器协议"""
        text = self.text.strip()
        if not text:
            yield DoubaoTranslated(self.src, self.dest, text, text)
            return

        if self.src == 'auto':
            try:
                detected = await self.translator.doubao_detect(text)
                self.src = detected.lang
            except Exception as e:
                logger.warning(f"Language detection failed, using 'auto': {str(e)}")

        prompt = f"将以下{self.src}文本翻译成{self.dest}：\n{text}"
        messages = [
            {"role": "system", "content": self.translator.system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response_stream = await self.translator._make_request(messages, stream=True)
            translated_text = ""
            async for chunk in response_stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    translated_text += chunk.choices[0].delta.content
                    yield DoubaoTranslated(self.src, self.dest, text, translated_text)
        except Exception as e:
            logger.error(f"Streaming translation failed: {str(e)}")
            raise DoubaoAPIError(f"流式翻译失败: {str(e)}")

# 使用示例
async def main():
    # 从环境变量获取API密钥
    api_key = os.getenv('ARK_API_KEY')
    if not api_key:
        print("请设置环境变量 ARK_API_KEY")
        return
        
    # 创建豆包翻译器实例
    async with DoubaoTranslator(
        api_key=api_key,
        base_url="https://ark.cn-beijing.volces.com/api/v3"
    ) as doubao_translator:
        try:
            # 基本翻译
            print("\n----- 豆包基本翻译 -----")
            result = await doubao_translator.doubao_translate('你好，世界！', dest='en')
            print(result)

            # 指定源语言
            print("\n----- 豆包指定源语言翻译 -----")
            result = await doubao_translator.doubao_translate('Hello, world!', src='en', dest='zh')
            print(result)

            # 流式翻译
            print("\n----- 豆包流式翻译 -----")
            stream_translator = await doubao_translator.doubao_translate('你好，世界！', dest='en', stream=True)
            print("Streaming translation:", end='', flush=True)
            async for partial_result in stream_translator:
                print(f"\rPartial result: {partial_result.text}", end='', flush=True)
            print()  # 换行

            # 批量翻译
            print("\n----- 豆包批量翻译 -----")
            texts = ['你好', '世界', 'AI']
            results = await doubao_translator.translate_batch(texts, dest='en')
            for result in results:
                print(f"{result.origin} -> {result.text}")

            # 语言检测
            print("\n----- 豆包语言检测 -----")
            detection = await doubao_translator.doubao_detect('这是一个中文句子')
            print(detection)
            detection = await doubao_translator.doubao_detect('This is an English sentence')
            print(detection)

            # 增强的语言检测测试
            print("\n----- 增强的语言检测 -----")
            test_texts = [
                "这是一个中文句子，来试语言检测功能。",
                "This is an English sentence for testing language detection.",
                "これは日本語のテストです。",
                "이것은 한국어 테스트입니다.",
                "Это русский язык",
                "هذه جملة باللغة العربية.",
                "Dies ist ein deutscher Satz.",
                "C'est une phrase en français."
            ]
            
            for text in test_texts:
                try:
                    detection = await doubao_translator.doubao_detect_enhanced(text)
                    print(f"Text: {text[:30]}...")
                    print(f"Detection result: {detection}")
                    print()
                except Exception as e:
                    print(f"Error detecting language for '{text[:30]}...': {str(e)}")
                    print()

            # 术语表测试
            print("\n----- 术语表测试 -----")
            
            # 创建示例术语表
            glossary_data = {
                "AI": {
                    "en": "Artificial Intelligence",
                    "zh": "人工智能",
                    "ja": "人工知能"
                },
                "ML": {
                    "en": "Machine Learning",
                    "zh": "机器学习",
                    "ja": "機械学習"
                }
            }
            
            # 存储术语表
            with open('glossary.json', 'w', encoding='utf-8') as f:
                json.dump(glossary_data, f, ensure_ascii=False, indent=2)
            
            # 创建带术语表的翻译器
            async with DoubaoTranslator(
                api_key=api_key,
                base_url="https://ark.cn-beijing.volces.com/api/v3",
                glossary_path='glossary.json'
            ) as translator_with_glossary:
                # 测试术语表翻译
                test_texts = [
                    "人工智能和机器学习是现代科技的重要领域。",
                    "Artificial Intelligence and Machine Learning are important fields in modern technology."
                ]
                
                for text in test_texts:
                    try:
                        # 检测语言
                        detected = await translator_with_glossary.doubao_detect(text)
                        src = detected.lang
                        dest = 'en' if src == 'zh' else 'zh'
                        
                        # 使用术语表翻译
                        result = await translator_with_glossary.apply_glossary(text, src=src, dest=dest)
                        print(f"\nSource ({src}): {text}")
                        print(f"Translation ({dest}): {result.text}")
                    except Exception as e:
                        print(f"Error translating text: {str(e)}")

                # 上下文感知翻译测试
                print("\n----- 上下文感知翻译测试 -----")
                
                try:
                    # 测试场景1：歧义词翻译
                    context1 = "这篇文章讨论了苹果公司的发展历程。"
                    text1 = "苹果推出了革新性的产品。"
                    
                    result = await translator_with_glossary.translate_with_context(
                        text=text1,
                        context=context1,
                        dest='en'
                    )
                    print(f"\nContext: {context1}")
                    print(f"Text: {text1}")
                    print(f"Translation: {result.text}")

                    # 测试场景2：专业文档翻译
                    context2 = "在机器学习领域，神经网络是一个重要的研究方向。"
                    text2 = "该网络的性能表现优异。"
                    
                    result = await translator_with_glossary.translate_with_context(
                        text=text2,
                        context=context2,
                        dest='en',
                        style_guide="使用学术论文的语气"
                    )
                    print(f"\nContext: {context2}")
                    print(f"Text: {text2}")
                    print(f"Translation: {result.text}")
                except Exception as e:
                    print(f"Error in context-aware translation: {str(e)}")

        except Exception as e:
            print(f"Error during testing: {str(e)}")
            raise

if __name__ == "__main__":
    asyncio.run(main())

