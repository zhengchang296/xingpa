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
    match = re.search(r'(.*?)(_0*)(\d+)(\.png)$', first_file_name)

    if not match:
        print(f"Error: The first file '{first_file_name}' does not match the expected pattern. Unable to infer renaming pattern.")
        print("Ensure that the file name ends with a numeric sequence followed by '.png'. Example: 'Walk-back_0001.png'.")
        return

    prefix, zero_padding, number, extension = match.groups()
    number_length = len(zero_padding) + len(number)

    print(f"Renaming files in {directory} based on the pattern of {first_file_name}...")

    # 排序并直接重命名文件
    new_number = 0  # 从编号 0 开始，您可以更改为其他初始编号
    renamed_files = []  # 用于记录重命名后的文件

    for file_name in files:
        match = re.search(r'(.*?)(_0*)(\d+)(\.png)$', file_name)
        if match:
            current_path = os.path.join(directory, file_name)
            
            # 构造新的文件名
            new_number += 1
            new_name = f"{prefix}_{str(new_number).zfill(number_length)}{extension}"
            new_path = os.path.join(directory, new_name)
            
            if current_path == new_path:
                print(f"File '{file_name}' already has the correct name. Skipping...")
                renamed_files.append(file_name)
                continue
            
            if os.path.exists(new_path):
                print(f"Error: Cannot rename {file_name} -> {new_name} (Target file already exists).")
                return

            # 执行文件重命名
            os.rename(current_path, new_path)
            renamed_files.append(new_name)
            print(f"Renamed '{file_name}' -> '{new_name}'")
        else:
            print(f"Skipping {file_name}: File name does not match the numeric pattern.")

    print("\nRenaming complete. Updated files:")
    for name in renamed_files:
        print(f" - {name}")

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing PNG files: ").strip()
    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]
    rename_files_in_directory(directory)