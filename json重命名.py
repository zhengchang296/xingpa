import os
import re
import json

def modify_json_files_then_rename(directory):
    """
    修改 JSON 文件内容中的 m_Name 字段，使其数字部分递增，
    然后根据修改后的 m_Name 修改对应的文件名。

    参数:
        directory (str): 包含 JSON 文件的目录路径。
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

    print(f"开始处理文件夹：{directory}")

    # 提取数字部分的位数（根据第一个文件推断）
    match = re.search(r"(.*?)(\d+)(.*)(\..+)", files[0])
    if not match:
        print(f"错误：第一个文件 '{files[0]}' 不符合命名规则。确保文件名中包含数字部分！")
        return

    prefix = match.group(1)  # 提取文件名前缀
    num_digits = len(match.group(2))  # 数字的位数
    postfix = match.group(3)  # 填充在数字之后的部分
    extension = match.group(4)  # 文件扩展名

    # 逐一处理 JSON 文件
    for index, file_name in enumerate(files):
        original_path = os.path.join(directory, file_name)

        # 生成递增的新数字
        new_number = str(index).zfill(num_digits)

        # 打开并修改 JSON 文件内容
        try:
            with open(original_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查并修改 m_Name 字段
            if "m_Name" in data:
                current_name = data["m_Name"]
                # 提取 m_Name 的前缀
                name_prefix = re.match(r"(.*?)(_?\d+)", current_name)
                if name_prefix:
                    new_m_name = f"{name_prefix.group(1)}_{new_number}"
                    data["m_Name"] = new_m_name
                else:
                    print(f"错误：文件 '{file_name}' 中的 m_Name 字段不包含可解析的数字部分，跳过该文件。")
                    continue
            
            # 如果字段不存在则提示错误
            else:
                print(f"文件 '{file_name}' 中未找到 m_Name 字段，跳过该文件。")
                continue

            # 保存更新后的 JSON 文件
            with open(original_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 根据新的 m_Name 转换文件名
            new_name = f"{data['m_Name']}{postfix}{extension}"
            new_path = os.path.join(directory, new_name)

            # 重命名文件
            os.rename(original_path, new_path)
            print(f"已修改并重命名文件：'{file_name}' -> '{new_name}'")

        except json.JSONDecodeError:
            print(f"错误：文件 {file_name} 不是有效的 JSON 文件，已跳过。")
        except Exception as e:
            print(f"处理文件 '{file_name}' 时发生错误：{e}")

    print("\n所有 JSON 文件已按顺序重命名并修改！")

if __name__ == "__main__":
    # 提示用户输入 JSON 文件夹路径
    directory = input("请输入包含 JSON 文件的目录路径：").strip()
    
    # 去掉目录路径中的额外引号（如有）
    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]
    
    modify_json_files_then_rename(directory)
