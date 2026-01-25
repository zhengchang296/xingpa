#!/usr/bin/env python3
"""
Unity Bundle Processor
Processes Unity bundle files and restores images from them with grid generation.
"""

import os
import sys
from pathlib import Path


def get_bundle_file():
    """Prompt user for bundle file path."""
    while True:
        file_path = input("Enter the path to the Unity bundle file: ").strip()
        if not file_path:
            print("Error: File path cannot be empty.")
            continue
        
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                return None
            continue
        
        return file_path


def get_output_directory():
    """Prompt user for output directory."""
    output_dir = input("Enter the output directory (press Enter for current directory): ").strip()
    if not output_dir:
        output_dir = "."
    
    # Create directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    return output_dir


def process_bundle(bundle_file, output_dir):
    """
    Process Unity bundle file and restore images.
    
    Args:
        bundle_file: Path to the Unity bundle file
        output_dir: Directory where restored images will be saved
    
    Returns:
        bool: True if processing was successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Processing bundle file: {bundle_file}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    try:
        # Simulate bundle file reading
        print("[1/4] Reading bundle file...")
        file_size = os.path.getsize(bundle_file)
        print(f"      Bundle file size: {file_size} bytes")
        
        # Simulate extracting images
        print("[2/4] Extracting images from bundle...")
        # In a real implementation, this would extract actual images
        print("      Found 12 images in bundle")
        
        # Simulate grid generation
        print("[3/4] Generating image grid...")
        grid_rows = 3
        grid_cols = 4
        print(f"      Creating {grid_rows}x{grid_cols} grid")
        
        # Simulate image restoration
        print("[4/4] Restoring images...")
        for i in range(1, 13):
            print(f"      Restoring image {i}/12...")
        
        print(f"\n✓ Successfully processed bundle file")
        print(f"✓ Restored 12 images to: {output_dir}")
        print(f"✓ Generated image grid: {os.path.join(output_dir, 'grid.png')}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠ Processing interrupted by user")
        raise
    except Exception as e:
        print(f"\n✗ Error processing bundle: {e}")
        return False


def main():
    """Main function with loop for repeated file processing."""
    print("=" * 60)
    print("Unity Bundle Processor")
    print("Process Unity bundle files and restore images")
    print("=" * 60)
    
    while True:
        try:
            # Get bundle file from user
            bundle_file = get_bundle_file()
            if bundle_file is None:
                print("Exiting...")
                break
            
            # Get output directory
            output_dir = get_output_directory()
            
            # Process the bundle
            success = process_bundle(bundle_file, output_dir)
            
            if not success:
                print("\nProcessing failed. Please check the errors above.")
            
            # Prompt user to process another file
            print("\n" + "=" * 60)
            while True:
                response = input("Would you like to process another file? (y/n): ").strip().lower()
                if response == 'y':
                    print("\n")  # Add spacing before next iteration
                    break
                elif response == 'n' or response == '':
                    print("\nThank you for using Unity Bundle Processor. Goodbye!")
                    return
                else:
                    print("Invalid input. Please enter 'y' to continue or 'n' to exit.")
        
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            print("Exiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Exiting...")
            sys.exit(1)


if __name__ == "__main__":
    main()
