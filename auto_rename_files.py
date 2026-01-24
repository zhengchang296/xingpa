import os
import re

def rename_images(directory):
    images = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images.sort()  # Sort files to ensure correct order

    # Determine the format using the first image
    if images:
        first_image = images[0]
        number_format = re.search(r'\d+', first_image)
        if number_format:
            leading_zeros = len(number_format.group(0))
    
    for index, image in enumerate(images):
        if images:
            # Determine new file name with leading zeros
            new_index = str(index + 1).zfill(leading_zeros)  # Match leading zeros
            new_name = re.sub(r'\d+', new_index, image)
            os.rename(os.path.join(directory, image), os.path.join(directory, new_name))
            print(f'Renamed: {image} -> {new_name}')  # Logging for reference

# Usage
# rename_images('path_to_your_images')
