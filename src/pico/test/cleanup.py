import os

def micropython_delete_all(path):
    for file in os.listdir(path):
        file_path = path + "/" + file
        try:
            os.remove(file_path)  # Try deleting as a file
        except OSError:
            micropython_delete_all(file_path)  # If it's a directory, recurse
            os.rmdir(file_path)  # Delete empty directory

# Delete everything in root
micropython_delete_all("/")
