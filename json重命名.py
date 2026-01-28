import os
import re
import json

def rename_json_files_and_update_name(directory):
    if not os.path.isdir(directory):
        print(f"错误：路径 '{directory}' 不是一个有效的目录。")
        return

    # 获取所有 JSON 文件并按名称排序
    files = [file for file in os.listdir(directory) if file.lower().endswith('.json')]
    files.sort()

    if not files:
        print("文件夹中未找到 JSON 文件。")
        return

    # 从第一个 JSON 文件提取前缀和数字部分的长度
    match = re.search(r"(.*?)(\d+)(\..+)", files[0])
    if match:
        prefix = match.group(1)  # 提取非数字的前缀部分
        num_digits = len(match.group(2))  # 提取数字部分的位数长度
        extension = match.group(3)  # 提取文件扩展名
    else:
        print(f"错误：第一个文件 '{files[0]}' 不包含可识别的数字部分。")
        return

    # 依次重命名每个 JSON 文件并更新 m_Name 内的数字
    for index, file_name in enumerate(files):
        original_path = os.path.join(directory, file_name)

        # 构建新的文件名
        new_number = str(index).zfill(num_digits)  # 使用与第一文件一致的数字长度
        new_name = f"{prefix}{new_number}{extension}"
        new_path = os.path.join(directory, new_name)

        # 打开并更新 JSON 文件内容
        try:
            with open(original_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # 检查是否存在 m_Name 字段并替换其中的数字
            if "m_Name" in json_data:
                json_data["m_Name"] = re.sub(r"\d+", new_number, json_data["m_Name"])
            
            # 将更新后的数据写入原文件
            with open(original_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        
            # 重命名文件
            os.rename(original_path, new_path)
            print(f"已重命名文件：'{file_name}' -> '{new_name}' 且更新 m_Name 为 '{json_data['m_Name']}'")
        except json.JSONDecodeError:
            print(f"错误：文件 '{file_name}' 不是有效的 JSON 文件，已跳过。")
        except Exception as e:
            print(f"重命名或修改文件 '{file_name}' 时发生错误：{e}")

    print("\n所有 JSON 文件已成功重命名并修改！")

if __name__ == "__main__":
    # 提示用户输入 JSON 文件夹路径
    directory = input("请输入包含 JSON 文件的文件夹路径：").strip()
    
    # 去掉路径中的额外引号（如果存在）
    if directory.startswith('\\"') and directory.endswith('\\"'):
        directory = directory[1:-1]

    rename_json_files_and_update_name(directory)
