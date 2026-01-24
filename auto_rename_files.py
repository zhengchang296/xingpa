import os
import re

def rename_files_in_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    # Get all png files in the directory
    files = [f for f in sorted(os.listdir(directory)) if f.endswith('.png')]

    if not files:
        print("No PNG files found in the directory.")
        return

    # Use the first file name as a base for renaming format
    first_file_name = files[0]
    match = re.search(r'(.*?)(\d+)(\.png)$', first_file_name)

    if not match:
        print(f"Error: The first file '{first_file_name}' does not contain a numeric pattern. Unable to infer renaming pattern.")
        return

    prefix, number, extension = match.groups()
    number_length = len(number)

    print(f"Renaming files in {directory} based on the pattern of {first_file_name}.")

    # Rename files with incremental numbers
    new_number = 1
    for file_name in files:
        match = re.search(r'(.*?)(\d+)(\.png)$', file_name)
        if match:
            current_prefix, current_number, current_extension = match.groups()
            new_name = f"{prefix}{str(new_number).zfill(number_length)}{extension}\n"

            # Avoid overwriting existing files
            new_path = os.path.join(directory, new_name)
            if os.path.exists(new_path):
                print(f"Skipping {file_name}: Target file {new_name} already exists.")
                continue

            # Perform rename
            current_path = os.path.join(directory, file_name)
            os.rename(current_path, new_path)
            print(f"Renamed {file_name} -> {new_name}")

            new_number += 1
        else:
            print(f"Skipping {file_name}: Does not match the pattern.")

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing PNG files: ")
    rename_files_in_directory(directory)