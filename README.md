# Test-task

README
# Folder Synchronization Tool

This script provides a tool for synchronizing the contents of a source folder to a replica folder. The tool works recursively through subdirectories, copying, updating or deleting files as necessary to ensure the contents of both folders remain identical.

The script uses the following functions:

* `copy_file`: to copy files from the source to the replica folder.
* `update_file`: to update files in the replica folder with new content from the source folder.
* `delete_file`: to delete files from the replica folder that do not exist in the source folder.
* `create_folder`: to create folders in the replica folder that do not exist in the source folder.
* `delete_folder`: to delete folders from the replica folder that do not exist in the source folder.
* `files`: to synchronize files in a folder.
* `folders`: to synchronize files and folders recursively in a directory.

## How to use the script

1. Make sure Python is installed on your computer.
2. Download the `folder_sync.py` script.
3. Open the command prompt or terminal and navigate to the directory containing the `folder_sync.py` script.
4. Run the following command to start the synchronization tool:
```bash
$ python folder_sync.py
```
5. The script will prompt you to enter the source folder path, replica folder path, synchronization interval in seconds, and log file path (The prompt for log file must be path/"log.txt"). Enter the requested information.
7. The script will run indefinitely, synchronizing the source and replica folders at the specified interval and logging the results to the specified log file.
### Exemple
```
Enter the source folder path: source
Enter the replica folder path: replica
Enter the synchronization interval in seconds: 10
Enter the log file path: log.txt
```

## Dependencies

This script requires the following Python packages to be installed:

* shutil
* logging
* os
* sys
* hashlib
* time
