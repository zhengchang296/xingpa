import os
import re

def rename_files(directory):
    
    # Change the working directory to the specified one
    os.chdir(directory)

    # Get a list of all the image files in the directory
    files = [f for f in os.listdir() if re.match(r".*\.(jpg|jpeg|png|gif)$", f, re.I)]

    # Sort files for consistent renaming
    files.sort()  
    
    # Determine the number of digits needed for numbering
    num_files = len(files)
    num_digits = len(str(num_files))
    
    # Rename the files
    for index, file in enumerate(files):
        # Create new filename with consistent digit lengths
        new_name = f"image_{str(index + 1).zfill(num_digits)}{os.path.splitext(file)[1]}"
        os.rename(file, new_name)
        print(f"Renamed '{file}' to '{new_name}'")

# Example usage:
# rename_files('path/to/your/images')
