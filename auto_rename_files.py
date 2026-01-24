import os
import re

def rename_files_in_directory(directory):
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        return

    # Retrieve all .png files in the directory and sort them based on system order
    image_files = [f for f in sorted(os.listdir(directory)) if f.lower().endswith('.png')]

    if not image_files:
        print("No PNG files found in the specified directory.")
        return

    # Use the first image file to determine renaming pattern
    first_file_name = image_files[0]
    match = re.search(r"(.*?)(_0*)(\d+)(\.png)$", first_file_name)

    if not match:
        print(f"Error: The first file '{first_file_name}' does not match the expected pattern.")
        return

    # Extract components from the first file name
    prefix, zero_padding, start_number_str, extension = match.groups()
    start_number = int(start_number_str)
    number_length = len(start_number_str)  # Determine length of number part, e.g., 003 = 3 digits

    print(f"The first file '{first_file_name}' will remain unchanged, starting numbering from {start_number}...")

    # Loop through images and rename starting with the second file
    next_number = start_number + 1
    for file_name in image_files[1:]:
        current_path = os.path.join(directory, file_name)

        # Construct new name
        new_name = f"{prefix}_{str(next_number).zfill(number_length)}{extension}"
        new_path = os.path.join(directory, new_name)

        if os.path.exists(new_path):
            print(f"Skipping '{file_name}': '{new_name}' already exists.")
        else:
            os.rename(current_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}'")

        next_number += 1

    print("\nRenaming complete.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing PNG files: ").strip()

    if directory.startswith('"') and directory.endswith('"'):
        directory = directory[1:-1]

    rename_files_in_directory(directory)