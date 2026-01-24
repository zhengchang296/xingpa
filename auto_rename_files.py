import os
import re

def rename_files_in_directory(directory):
    if not os.path.isdir(directory):
        print(f'Error: {directory} is not a valid directory.')
        return

    # 获取目录中以 .png 结尾的所有文件
    files = [f for f in sorted(os.listdir(directory)) if f.endswith('.png')]

    if not files:
        print('No PNG files found in the directory.')
        return

    # 使用文件的第一个名字推断命名规则
    first_file_name = files[0]
    match = re.search(r'(.*?)(_0*)(\d+)(\.png)$', first_file_name)

    if not match:
        print(f'Error: The first file \'{first_file_name}\' does not match the expected pattern. Unable to infer renaming pattern.')
        return

    prefix, zero_padding, number, extension = match.groups()
    number_length = len(zero_padding) + len(number)

    print(f'Renaming files in {directory} based on the pattern of {first_file_name}.')

    # 重命名文件，按递增序号从 1 开始重新命名
    new_number = 1
    for file_name in files:
        match = re.search(r'(.*?)(_0*)(\d+)(\.png)$', file_name)
        if match:
            current_prefix, current_zero_padding, current_number, current_extension = match.groups()
            new_name = f"{prefix}_{str(new_number).zfill(number_length)}{extension}"

            # 确保避免文件覆盖
            current_path = os.path.join(directory, file_name)
            new_path = os.path.join(directory, new_name)
            
            if os.path.exists(new_path):
                print(f'Skipping {file_name}: Target file \'{new_name}\' already exists.')
                continue

            # 执行重命名
            os.rename(current_path, new_path)
            print(f'Renamed {file_name} -> {new_name}')

            new_number += 1
        else:
            print(f'Skipping {file_name}: File name does not match the pattern.')

if __name__ == "__main__":
    directory = input('Enter the path to the directory containing PNG files: ').strip()
    rename_files_in_directory(directory)