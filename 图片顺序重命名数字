import os
import re

def rename_images_with_prefix_and_digits(directory):
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        return

    # 获取目录内的所有图片文件，并按名称排序
    files = [file for file in os.listdir(directory) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    files.sort()

    if not files:
        print("No image files found in the directory.")
        return

    # 从第一张图片文件提取前缀和数字部分的长度
    match = re.search(r"(.*?)(\d+)(\..+)", files[0])
    if match:
        prefix = match.group(1)  # 提取非数字的前缀部分
        num_digits = len(match.group(2))  # 提取数字部分的位数长度
        extension = match.group(3)  # 提取文件扩展名
    else:
        print(f"Error: The first file '{files[0]}' does not contain a recognizable numeric part.")
        return

    # 依次重命名图片文件
    for index, file_name in enumerate(files):
        original_path = os.path.join(directory, file_name)

        # 构建新文件名
        new_number = str(index).zfill(num_digits)  # 保持数字部分与第一张图片一致
        new_name = f"{prefix}{new_number}{extension}"
        new_path = os.path.join(directory, new_name)

        # 执行重命名操作
        try:
            os.rename(original_path, new_path)
            print(f"Renamed: '{file_name}' -> '{new_name}'")
        except Exception as e:
            print(f"Error renaming file '{file_name}': {e}")

    print("\nRenaming complete! All images have been renamed successfully.")

if __name__ == "__main__":
    # 提示用户输入图片文件夹路径
    directory = input("Enter the path to the directory containing images: ").strip()
    
    # 去掉路径中的额外引号（如果存在）
    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]

    rename_images_with_prefix_and_digits(directory)
