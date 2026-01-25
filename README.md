# Unity Bundle Processor

A Python script for processing Unity bundle files and restoring images from them with grid generation capabilities.

## Features

- Process Unity bundle files to extract and restore images
- Automatic grid generation for extracted images
- Interactive loop functionality for processing multiple files
- Robust error handling and user-friendly prompts
- Support for custom output directories

## Usage

### Basic Usage

Run the script directly:

```bash
python3 unity_bundle_processor.py
```

Or make it executable and run:

```bash
chmod +x unity_bundle_processor.py
./unity_bundle_processor.py
```

### Workflow

1. The script will prompt you for the path to a Unity bundle file
2. It will ask for an output directory (press Enter for current directory)
3. The script processes the bundle file through 4 stages:
   - Reading bundle file
   - Extracting images from bundle
   - Generating image grid
   - Restoring images
4. After completion, you'll be asked if you want to process another file
   - Enter `y` to process another file
   - Enter `n` or press Enter to exit the program
   - Invalid inputs will prompt you to try again

### Example Session

```
============================================================
Unity Bundle Processor
Process Unity bundle files and restore images
============================================================
Enter the path to the Unity bundle file: /path/to/bundle.unity
Enter the output directory (press Enter for current directory): /path/to/output

============================================================
Processing bundle file: /path/to/bundle.unity
Output directory: /path/to/output
============================================================

[1/4] Reading bundle file...
      Bundle file size: 1024 bytes
[2/4] Extracting images from bundle...
      Found 12 images in bundle
[3/4] Generating image grid...
      Creating 3x4 grid
[4/4] Restoring images...
      Restoring image 1/12...
      ...

✓ Successfully processed bundle file
✓ Restored 12 images to: /path/to/output
✓ Generated image grid: /path/to/output/grid.png

============================================================
Would you like to process another file? (y/n): y

Enter the path to the Unity bundle file: ...
```

## Error Handling

- **File Not Found**: If the specified bundle file doesn't exist, you'll be asked if you want to try again
- **Keyboard Interrupt**: Press Ctrl+C to cancel processing at any time
- **Processing Errors**: Any errors during processing are caught and displayed with appropriate messages

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)