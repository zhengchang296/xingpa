import os
import re
import json

def rename_json_files_and_update_fields(directory, new_path_id):
    """
    重命名 JSON 文件使文件名的数字部分递增，并同时修改 JSON 内容中的 m_Name 和 m_PathID 字段。

    参数:
        directory (str): 包含 JSON 文件的目录路径。
        new_path_id (int): 替换所有文件中 m_PathID 的新值。
    """
    if not os.path.isdir(directory):
        print(f"错误：路径 '{directory}' 不是一个有效的目录。")
        return

    # 获取所有 JSON 文件并按名称排序
    files = [file for file in os.listdir(directory) if file.lower().endswith('.json')]
    files.sort()

    if not files:
        print("文件夹中未找到 JSON 文件。")
        return

    # 提取数字部分的长度（根据第一个文件推断）
    match = re.search(r"(.*?)(\d+)(\..+)", files[0])
    if match:
        prefix = match.group(1)  # 提取非数字部分的前缀
        num_digits = len(match.group(2))  # 数字部分的位数，例如5位数 -> 00000
        extension = match.group(3)  # 文件扩展名
    else:
        print(f"错误：第一个文件 '{files[0]}' 不包含可识别的数字部分。")
        return

    # 按序重命名文件，并更新文件内容
    for index, file_name in enumerate(files):
        original_path = os.path.join(directory, file_name)

        # 生成新的文件名，格式如 'prefix00001.extension'
        new_number = str(index).zfill(num_digits)  # 生成递增的数字
        new_name = f"{prefix}{new_number}{extension}"
        new_path = os.path.join(directory, new_name)

        # 修改 JSON 文件内容
        try:
            with open(original_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 更新 m_Name 和 m_PathID 的值
            if "m_Name" in data:
                data["m_Name"] = f"{prefix}{new_number}"
            if "m_RD" in data and "texture" in data["m_RD"] and "m_PathID" in data["m_RD"]["texture"]:
                data["m_RD"]["texture"]["m_PathID"] = new_path_id

            # 将修改后的内容写回文件
            with open(original_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 重命名文件
            os.rename(original_path, new_path)
            print(f"文件 '{file_name}' 已重命名为 '{new_name}'，并更新 m_Name 为 '{data['m_Name']}', m_PathID 为 '{new_path_id}'")

        except json.JSONDecodeError:
            print(f"错误：文件 '{file_name}' 不是有效的 JSON 文���，已跳过。")
        except Exception as e:
            print(f"重命名或修改文件 '{file_name}' 时发生错误：{e}")

    print("\n所有 JSON 文件已成功重命名并修改！")

if __name__ == "__main__":
    # 提示用户输入 JSON 文件的目录路径
    directory = input("请输入包含 JSON 文件的目录路径：").strip()
    
    # 去掉目录路径中的额外引号（如有）
    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]
    
    # 提示用户输入新的 PathID
    try:
        new_path_id = int(input("请输入新的 PathID 值：").strip())
        rename_json_files_and_update_fields(directory, new_path_id)
    except ValueError:
        print("错误：PathID 必须是一个数字！")
