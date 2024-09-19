import json
import re
from googletrans import Translator

def is_url(string):
    # 使用正则表达式检查字符串是否为网址
    url_pattern = re.compile(r'http[s]?://\S+')
    return re.match(url_pattern, string) is not None

def translate_description(obj, translator):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'description' and isinstance(value, str):
                if is_url(value):  # 检查是否为网址
                    print(f'跳过网址: {value}')
                    continue
                print(f'翻译: {value}')
                try:
                    translated = translator.translate(value, src='en', dest='zh-cn')
                    obj[key] = translated.text
                except Exception as e:
                    print(f"翻译失败: {e}")
            else:
                translate_description(value, translator)
    elif isinstance(obj, list):
        for item in obj:
            translate_description(item, translator)

def main():
    input_file = 'libraries.json'          # 输入的 JSON 文件路径
    output_file = 'libraries_translated.json'  # 输出的 JSON 文件路径

    try:
        # 读取 JSON 文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误: 无法找到文件 {input_file}")
        return
    except json.JSONDecodeError:
        print(f"错误: {input_file} 包含无效的 JSON 格式")
        return

    translator = Translator()

    # 翻译 description 字段
    translate_description(data, translator)

    try:
        # 写入新的 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"写入文件失败: {e}")
        return

    print(f'翻译完成，结果已保存到 {output_file}')

if __name__ == '__main__':
    main()