from doubaotrans import DoubaoTranslator
import os
import asyncio
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

async def main():
    # 初始化翻译器
    translator = DoubaoTranslator(
        api_key=os.getenv('ARK_API_KEY'),
        performance_mode='accurate'
    )

    # 术语表示例
    translator.add_term("AI", {
        "en": "Artificial Intelligence",
        "zh": "人工智能"
    })

    # 异步批量翻译
    texts = [
        "AI is transforming our world",
        "Machine learning is the future",
        "Data science is essential"
    ]
    
    results = await translator.translate_batch_async(
        texts=texts,
        dest="zh",
        batch_size=2
    )
    
    for text, result in zip(texts, results):
        print(f"原文: {text}")
        print(f"译文: {result.text}\n")

if __name__ == "__main__":
    asyncio.run(main())