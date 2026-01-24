import os

def rename_image_files(directory):
    # Fetch all image files from the directory
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Sort files to maintain the order
    image_files.sort()

    # Check if there are any images to rename
    if not image_files:
        print("No image files found in the specified directory.")
        return

    # Keep the first file name unchanged
    base_name, extension = os.path.splitext(image_files[0])
    new_file_names = [image_files[0]]  # First file remains unchanged

    # Increment the numerical suffix for the remaining files
    for i in range(1, len(image_files)):
        # Extract the base name and numerical suffix
        suffix = str(i + 1).zfill(len(base_name.split('_')[-1]))  # Ensure it maintains number length
        new_file_name = f"{base_name[:-len(base_name.split('_')[-1])]}{suffix}{extension}"
        new_file_names.append(new_file_name)

        # Rename the file
        os.rename(os.path.join(directory, image_files[i]), os.path.join(directory, new_file_name))

    print("Files have been renamed successfully:", new_file_names)

# Example usage:
# rename_image_files('/path/to/your/images')