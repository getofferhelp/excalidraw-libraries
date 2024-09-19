import json

def merge_descriptions(original_file, translated_file, output_file):
    try:
        # 读取原始 JSON 文件
        with open(original_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # 读取翻译后的 JSON 文件
        with open(translated_file, 'r', encoding='utf-8') as f:
            translated_data = json.load(f)

        # 合并描述
        def combine_descriptions(obj_original, obj_translated):
            if isinstance(obj_original, dict) and isinstance(obj_translated, dict):
                for key in obj_original.keys():
                    if key == 'description' and isinstance(obj_original[key], str):
                        original_desc = obj_original[key]
                        translated_desc = obj_translated[key]

                        # 创建新的描述格式
                        combined_desc = f"中文翻译：{translated_desc}\n\n英文原文：{original_desc}"
                        obj_original[key] = combined_desc
                    else:
                        combine_descriptions(obj_original[key], obj_translated.get(key, {}))
            elif isinstance(obj_original, list) and isinstance(obj_translated, list):
                for item_original, item_translated in zip(obj_original, obj_translated):
                    combine_descriptions(item_original, item_translated)

        # 合并描述内容
        combine_descriptions(original_data, translated_data)

        # 写入新的 JSON 文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(original_data, f, ensure_ascii=False, indent=4)

        print(f'合并完成，结果已保存到 {output_file}')

    except FileNotFoundError as e:
        print(f"错误: 找不到文件 {e.filename}")
    except json.JSONDecodeError:
        print(f"错误: JSON 格式无效")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    original_file = 'libraries.json'              # 原始 JSON 文件路径
    translated_file = 'libraries_translated.json' # 翻译后的 JSON 文件路径
    output_file = 'libraries3.json'               # 输出的合并后 JSON 文件路径

    merge_descriptions(original_file, translated_file, output_file)