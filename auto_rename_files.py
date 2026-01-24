import os
import re

def rename_files_in_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    # 获取目录中以 .png 结尾的所有文件，依据系统自然排序
    files = [f for f in sorted(os.listdir(directory)) if f.lower().endswith('.png')]

    if not files:
        print("No PNG files found in the directory.")
        return

    # 从第一个文件的名字推断命名规则
    first_file_name = files[0]
    match = re.search(r'(.*?)(_0*)(\n+)(\.png)$', first_file_name)

    if not match:
        print(f"Error: The first file '{first_file_name}' does not match the expected pattern. Unable to infer renaming pattern.")
        print("Ensure that the file name ends with a numeric sequence followed by '.png'. Example: 'Walk-back_0001.png'.")
        return

    prefix, zero_padding, number, extension = match.groups()
    number_length = len(zero_padding) + len(number)

    print(f"Renaming files in {directory} based on the pattern of {first_file_name}...")

    # 排序并直接重命名文件
    new_number = int(number)  # 从编号开始，您可以更改为其他初始编号
