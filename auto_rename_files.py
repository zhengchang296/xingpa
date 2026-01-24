import os
import re

def rename_files_in_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    # 获取目录中以 .png 结尾的所有文件，按字典序排序
    files = [f for f in sorted(os.listdir(directory)) if f.lower().endswith('.png')]

    if not files:
        print("No PNG files found in the directory.")
        return

    # 确保第一个文件的命名保持不变
    first_file_name = files[0]
    match = re.search(r'(.*?)(_0*)(\d+)(\.png)$', first_file_name)

    if not match:
        print(f"Error: The first file '{first_file_name}' does not match the expected pattern. Skipping renaming.")
        return

    prefix, zero_padding, number, extension = match.groups()
    number_length = len(zero_padding) + len(number)

    print(f"The first file '{first_file_name}' is assumed to be correctly named and will not be modified.")

    new_number = int(number) + 1

    # 从第二个文件开始进行重命名
    for file_name in files[1:]:
        match = re.search(r'(.*?)(_0*)(\d+)(\.png)$', file_name)
        if match:
            current_path = os.path.join(directory, file_name)

            new_name = f"{prefix}_{str(new_number).zfill(number_length)}{extension}"
            new_path = os.path.join(directory, new_name)

            if current_path == new_path:
                print(f"File '{file_name}' already has the correct name. Skipping...")
                new_number += 1
                continue

            if os.path.exists(new_path):
                print(f"Skipping {file_name}: Target file '{new_name}' already exists.")
                new_number += 1
                continue

            # 执行文件重命名
            os.rename(current_path, new_path)
            print(f"Renamed '{file_name}' -> '{new_name}'")
            new_number += 1
        else:
            print(f"Skipping {file_name}: File name does not match the expected pattern.")

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing PNG files: ").strip()
    # 处理路径前后的引号
    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]
    rename_files_in_directory(directory)