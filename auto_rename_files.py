import os
import re

def rename_files_in_directory(directory):
    files = os.listdir(directory)
    files.sort()
    
    if not files:
        return
    
    # RegEx to match filenames with a numeric suffix
    num_pattern = r"_(\d+)$"
    
    # Keep the first file unchanged
    first_file = files[0]
    print(f"Keeping file: {first_file}")
    
    # Extract number from the first file name
    match = re.search(num_pattern, first_file)
    if match:
        number_length = len(match.group(1))
        base_name = first_file[:match.start()]
    else:
        base_name = first_file
        number_length = 0
    
    # Rename the remaining files
    for i, file in enumerate(files[1:], start=1):
        match = re.search(num_pattern, file)
        new_number = str(i).zfill(number_length) if number_length > 0 else ''
        new_file_name = f"{base_name}_{new_number}" if number_length > 0 else f"{base_name}"
        
        print(f"Renaming '{file}' to '{new_file_name}'")
        os.rename(os.path.join(directory, file), os.path.join(directory, new_file_name))

# Example usage
rename_files_in_directory('/path/to/directory')  # Replace with actual directory path
