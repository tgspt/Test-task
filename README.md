# Test-task

README
This script provides a folder synchronization tool that periodically copies files from a source folder to a replica folder, while keeping their contents identical. It works recursively through subdirectories.

Functions
The script uses the following functions:

copy_file: to copy files from the source to the replica folder.
update_file: to update files in the replica folder with new content from the source folder.
delete_file: to delete files from the replica folder that do not exist in the source folder.
create_folder: to create folders in the replica folder that do not exist in the source folder.
delete_folder: to delete folders from the replica folder that do not exist in the source folder.
files: to synchronize files in a folder.
folders: to synchronize files and folders recursively in a directory.
Usage
To use this script, run it with the following command:

Copy code
python folder_sync.py
The script will then prompt you to enter the source folder path, replica folder path, synchronization interval in seconds, and log file path.

The script will then run indefinitely, synchronizing the source and replica folders at the specified interval and logging the results to the specified log file.

Logging
The logging module is used to log the status of the synchronization operations. Two logging handlers are used:

FileHandler: saves the log output to a file named "log.txt".
StreamHandler: outputs the log messages to the console.
Dependencies
This script has the following dependencies:

shutil
logging
os
sys
hashlib
time
