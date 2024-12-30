# DoubaoTranslator | 豆包翻译器

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.2-green.svg)](https://pypi.org/project/doubaotrans/)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

[English](#english) | [中文](#chinese)

---

<a id="english"></a>
## 🌍 English

DoubaoTranslator is a professional translation toolkit based on Doubao API, providing features such as multilingual translation, glossary management, context-aware translation, and style customization.

### Features

- **Multilingual Support**: Translation between 17 mainstream languages
- **Context-Aware Translation**: Maintains semantic coherence with context window
- **Glossary Management**: Custom terminology mapping for professional accuracy
- **Style Templates**: Predefined styles (formal, casual, technical, creative)
- **Streaming Translation**: Real-time translation with partial results
- **Batch Processing**: Efficient bulk translation with concurrency control
- **Enhanced Language Detection**: Combined results from multiple detectors
- **Performance Optimization**: Caching, retry mechanisms, HTTP/2 support
- **Document Translation**: Context-aware translation for long documents
- **Translation Evaluation**: Quality assessment functionality
- **Async Support**: Complete async operation support, including context managers

### Installation

```bash
pip install doubaotrans
```

### Quick Start

```python
from doubaotrans import DoubaoTranslator

# Initialize translator
translator = DoubaoTranslator(api_key="your_api_key")

# Basic translation
result = await translator.doubao_translate("Hello, World!", dest="zh")
print(result.text)  # 你好，世界！

# Batch translation
texts = ["Hello", "World", "AI"]
results = await translator.translate_batch(texts, dest="zh")
for result in results:
    print(f"{result.origin} -> {result.text}")

# Context-aware translation
context = "This article discusses the history of Apple Inc."
text = "Apple released an innovative product."
result = await translator.translate_with_context(
    text=text,
    context=context,
    dest="zh"
)
print(result.text)  # Will translate "Apple" as the company, not the fruit
```

For detailed documentation and examples, please visit our [GitHub repository](https://github.com/kilolonion/Doubaotranslator).

---

<a id="chinese"></a>
## 🌏 中文

DoubaoTranslator 是一个基于豆包 API 的专业翻译工具包，提供多语言翻译、术语表管理、上下文感知翻译和风格定制等功能。

### 功能特点

- **多语言支持**：支持 17 种主流语言之间的互译
- **上下文感知**：使用上下文窗口维持语义连贯性
- **术语管理**：自定义术语映射，确保专业准确性
- **风格模板**：预定义风格（正式、随意、技术、创意）
- **流式翻译**：实时翻译并返回部分结果
- **批量处理**：高效的批量翻译与并发控制
- **增强语言检测**：结合多个检测器提高准确率
- **性能优化**：缓存、重试机制、HTTP/2 支持
- **文档翻译**：支持长文档的上下文感知翻译
- **翻译评估**：提供翻译质量评估功能
- **异步支持**：完整的异步操作支持，包括上下文管理器

### 安装

```bash
pip install doubaotrans
```

### 快速开始

```python
from doubaotrans import DoubaoTranslator

# 初始化翻译器
translator = DoubaoTranslator(api_key="your_api_key")

# 基本翻译
result = await translator.doubao_translate("你好，世界！", dest="en")
print(result.text)  # Hello, World!

# 批量翻译
texts = ["你好", "世界", "人工智能"]
results = await translator.translate_batch(texts, dest="en")
for result in results:
    print(f"{result.origin} -> {result.text}")

# 上下文感知翻译
context = "这篇文章讨论了苹果公司的发展历程。"
text = "苹果推出了革新性的产品。"
result = await translator.translate_with_context(
    text=text,
    context=context,
    dest="en"
)
print(result.text)  # 会将"苹果"翻译为公司而不是水果
```

详细文档和示例请访问我们的 [GitHub 仓库](https://github.com/kilolonion/Doubaotranslator)。

---

## 📝 Notes | 注意事项

### English
1. API Limitations
   - Maximum text length per request: 5000 characters
   - API rate limiting may apply
   - Async methods recommended for handling large volumes

2. Performance Optimization
   - HTTP/2 support requires the `hyper` package
   - Caching mechanism reduces duplicate requests
   - Batch processing improves efficiency

### 中文
1. API 限制
   - 每次请求的最大文本长度：5000 字符
   - 可能受 API 速率限制
   - 建议使用异步方法处理大量请求

2. 性能优化
   - 使用 HTTP/2 需要安装 `hyper` 包
   - 缓存机制可以减少重复请求
   - 批量处理可以提高效率

## 📄 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 Acknowledgments | 致谢

- Thanks to all contributors
- 感谢所有贡献者

## 📧 Contact | 联系方式

- Author | 作者: kilon
- Email | 邮箱: a15607467772@163.com