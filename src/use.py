import os
from imutils import paths
from pathlib import Path

def delete_except(directory, exceptions):
    """
    Delete all files in a directory except the specified exceptions.

    :param directory: The directory to clean.
    :param exceptions: A list of filenames to exclude from deletion.
    """
    # Convert exceptions to Path objects for better compatibility
    exceptions_set = set(Path(except_path).resolve() for except_path in exceptions)

    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    for item in os.listdir(directory):
        item_path = Path(directory) / item

        # If it's a file and not in the exception set, delete it
        if item_path.is_file() and item_path.resolve() not in exceptions_set:
            try:
                item_path.unlink()  # Using pathlib's unlink to delete files
                print(f"Deleted: {item_path}")
            except Exception as e:
                print(f"Failed to delete {item_path}: {e}")

if __name__ == "__main__":
    # Directory to clean
    target_directory = "asset/wildPlastic/choose_datasets/labels"
    
    # List of files to keep
    files_to_keep = []   
    
    # Create a list of the annotation files to keep
    trnPaths = list(paths.list_images("asset/wildPlastic/choose_datasets/images"))
    for trnPath in trnPaths:
        imageID = Path(trnPath).stem  # Use pathlib to get the file name without extension
        annotation_file = Path("asset/wildPlastic/choose_datasets/labels") / f"{imageID}.txt"
        files_to_keep.append(annotation_file)
    
    # Debug: Check files to keep and their count
    print(files_to_keep)
    print(len(files_to_keep))
    
    # Execute deletion
    delete_except(target_directory, files_to_keep)
