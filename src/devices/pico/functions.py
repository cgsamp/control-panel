import os

def delete_all_files(directory="/"):
    for file in os.listdir(directory):
        path = directory + "/" + file
        try:
            if os.stat(path)[0] & 0x4000:  # Check if it's a directory
                delete_all_files(path)  # Recursively delete files in subdirectories
                os.rmdir(path)  # Remove empty directory
            else:
                os.remove(path)  # Remove file
            print(f"Deleted: {path}")
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

