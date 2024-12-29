from doubaotrans import DoubaoTranslator
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    # 初始化翻译器
    translator = DoubaoTranslator(
        api_key=os.getenv('ARK_API_KEY'),
        performance_mode='balanced'
    )

    # 基本翻译示例
    print("\n1. 基本翻译")
    result = translator.doubao_translate("Hello, world!", dest="zh")
    print(f"翻译结果: {result.text}")

    # 语言检测示例
    print("\n2. 语言检测")
    detection = translator.doubao_detect("这是中文文本")
    print(f"检测结果: {detection.lang}, 置信度: {detection.confidence}")

if __name__ == "__main__":
    main()