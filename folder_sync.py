"""
This script provides a folder synchronization tool that periodically copies files 
from a source folder to a replica folder, while keeping their contents identical. 
It works recursively through subdirectories.

The script uses the following functions:
- copy_file: to copy files from the source to the replica folder.
- update_file: to update files in the replica folder with new content from the source folder.
- delete_file: to delete files from the replica folder that do not exist in the source folder.
- create_folder: to create folders in the replica folder that do not exist in the source folder.
- delete_folder: to delete folders from the replica folder that do not exist in the source folder.
- files: to synchronize files in a folder.
- folders: to synchronize files and folders recursively in a directory.

To use this script, run it with the following command:

$ python folder_sync.py

The script will then prompt you to enter the source folder path, replica folder path, 
synchronization interval in seconds, and log file path. The script will then run indefinitely, 
synchronizing the source and replica folders at the specified interval and logging 
the results to the specified log file.
"""
import shutil
import logging
import os
import sys
import hashlib
import time

# The FileHandler() is used to setup the output file  for loggers other than the root logger.
# streamHandler() is used to output the in screen console
if not os.path.exists('log.txt'):
    open('log.txt', 'w').close()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(filename="log.txt", mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)

def file_hash(file_path):
    """Calculate the MD5 hash of the file content.

    Args:
        file_path (str): The path to the file to be hashed.

    Returns:
        str: The hexadecimal representation of the MD5 hash value.
    """
    with open(file_path, "rb") as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()


def copy_file(source_path, replica_path):
    """Copy the file at the given source path to the given replica path.

    Args:
        source_path (str): The path to the file to be copied.
        replica_path (str): The path where the copy of the file will be created.

    Returns:
        None.
    """
    shutil.copy2(source_path, replica_path)
    logging.info("Copied file:%s %s", source_path, replica_path)


def delete_file(replica_path):
    """Delete the file at the given path.

    Args:
        replica_path (str): The path to the file to be deleted.

    Returns:
        None.
    """
    os.remove(replica_path)
    logging.info("Deleted file:%s", replica_path)


def update_file(source_path, replica_path):
    """Update the file at the given replica path with the contents 
        of the file at the given source path.

    Args:
        source_path (str): The path to the file to be used as the new content.
        replica_path (str): The path to the file to be updated.

    Returns:
        None.
    """
    shutil.copy2(source_path, replica_path)
    logging.info("Updated file:%s %s", source_path, replica_path)


def create_folder(folder_path):
    """Create a new folder at the given path.

    Args:
        folder_path (str): The path to the folder to be created.

    Returns:
        None.
    """
    os.makedirs(folder_path)
    logging.info("Created Folder:%s", folder_path)


def delete_folder(folder_path):
    """Delete the folder at the given path, along with all its contents.

    Args:
        folder_path (str): The path to the folder to be deleted.

    Returns:
        None.
    """
    shutil.rmtree(folder_path)
    logging.info("Deleted Folder: %s", folder_path)


def files(source_folder_path, replica_folder_path):
    """Compare the contents of two folders and synchronize them.

    The `files` function compares the contents of two folders 
    specified by their paths, `source_folder_path` and
    `replica_folder_path`. It synchronizes the files in the two folders 
    by copying, updating or deleting files as necessary. 
    This function uses the `copy_file`, `update_file`, `delete_file`, 
    and `file_hash` helper functions.

    Args:
        source_folder_path (str): The path to the source folder containing the original files.
        replica_folder_path (str): The path to the replica folder to be updated.

    Returns:
        None.
    """
    source_files = [
        f
        for f in os.listdir(source_folder_path)
        if os.path.isfile(os.path.join(source_folder_path, f))
    ]
    replica_files = [
        f
        for f in os.listdir(replica_folder_path)
        if os.path.isfile(os.path.join(replica_folder_path, f))
    ]

    for source_file in source_files:
        source_file_path = os.path.join(source_folder_path, source_file)
        replica_file_path = os.path.join(replica_folder_path, source_file)

        if source_file not in replica_files:
            copy_file(source_file_path, replica_file_path)

        else:
            if file_hash(source_file_path) != file_hash(replica_file_path):
                update_file(source_file_path, replica_file_path)

    for replica_file in replica_files:
        replica_file_path = os.path.join(replica_folder_path, replica_file)

        if replica_file not in source_files:
            delete_file(replica_file_path)


def folders(source_folder_path, replica_folder_path):
    """Recursively synchronizes the source folder 
    with the replica folder, creating, updating or deleting files
    and folders as necessary. 
    The synchronization process is performed by calling the `files()` and `folders()`
    functions on each subfolder of the source and replica folders.

    Args:
        source_folder_path (str): The path to the source folder.
        replica_folder_path (str): The path to the replica folder.

    Returns:
        None.
    """

    if not os.path.exists(replica_folder_path):
        create_folder(replica_folder_path)

    files(source_folder_path, replica_folder_path)

    source_sub_folders = [
        f
        for f in os.listdir(source_folder_path)
        if os.path.isdir(os.path.join(source_folder_path, f))
    ]
    replica_sub_folders = [
        f
        for f in os.listdir(replica_folder_path)
        if os.path.isdir(os.path.join(replica_folder_path, f))
    ]

    for source_sub_folder in source_sub_folders:
        source_sub_folder_path = os.path.join(source_folder_path, source_sub_folder)
        replica_sub_folder_path = os.path.join(replica_folder_path, source_sub_folder)

        if source_sub_folder not in replica_sub_folders:
            create_folder(replica_sub_folder_path)

        folders(source_sub_folder_path, replica_sub_folder_path)

    for replica_sub_folder in replica_sub_folders:
        replica_sub_folder_path = os.path.join(replica_folder_path, replica_sub_folder)

        if replica_sub_folder not in source_sub_folders:
            delete_folder(replica_sub_folder_path)

def main():
    """Synchronize the contents of a source folder with a replica folder at regular intervals.

    Prompts the user to input the paths to the source and replica folders, 
    the synchronization interval in seconds, and the path to the log file.

    The function then starts a loop that synchronizes the folders 
    at the specified interval until the program is interrupted.

    Args:
        None

    Returns:
        None
    """
    source_folder_path = input("Enter the source folder path: ")
    replica_folder_path = input("Enter the replica folder path: ")
    sync_interval = int(
        input("Enter the synchronization interval in seconds: "))
    log_file_path = input("Enter the log file path: ")

    logging.getLogger().handlers[0].baseFilename = log_file_path

    while True:
        folders(source_folder_path, replica_folder_path)
        time.sleep(sync_interval)


if __name__ == "__main__":
    main()
