import shutil
import logging
import os
import sys
import hashlib
import time

#The FileHandler() is used to setup the output file  for loggers other than the root logger.
#streamHandler() is used to output the in screen console
logging.basicConfig(    
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(filename="test.txt", mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)
def fileHash(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
    return hashlib.md5(content).hexdigest()
#src=pathOriginal dst=pathReplica

def copyFile(sourcePath, replicaPath):
    shutil.copy2(sourcePath, replicaPath)
    logging.info(f"Copied file:{sourcePath, replicaPath}")


def deleteFile(replicaPath):
    os.remove(replicaPath)
    logging.info(f"Deleted file:{replicaPath}")

def updateFile(sourcePath, replicaPath):
    shutil.copy2(sourcePath, replicaPath)
    logging.info(f"Updated file:{sourcePath, replicaPath}")

def createFolder(folderPath):
    os.makedirs(folderPath)
    logging.info(f"Created Folder:{folderPath}")

def deleteFolder(folderPath):
    shutil.rmtree(folderPath)  
    logging.info(f"Deleted Folder:{folderPath}")

def files(sourceFolderPath, replicaFolderPath):
    #creating a list of all the files
    sourceFile = [f for f in os.listdir(sourceFolderPath) if os.path.isfile(os.path.join(sourceFolderPath, f))]
    replicaFile = [f for f in os.listdir(replicaFolderPath) if os.path.isfile(os.path.join(replicaFolderPath, f))]

    for sourceFile in sourceFile:
       
        sourceFilePath=os.path.join(sourceFolderPath, sourceFile)
        replicaFilePath=os.path.join(replicaFolderPath, sourceFile)
        
        if sourceFile not in replicaFile:
            
            copyFile(sourceFilePath, replicaFilePath)
        
        else:
            
            if fileHash(sourceFilePath) != fileHash(replicaFilePath):
                updateFile(sourceFilePath,replicaFilePath)
    
    for replicaFile in replicaFile:

        replicaFilePath=os.path.join(replicaFolderPath, replicaFile)
        
        if replicaFile not in sourceFile:
            deleteFile(replicaFilePath)

def folders(sourceFolderPath, replicaFolderPath):
    #creating a list of all the files
    files(sourceFolderPath, replicaFolderPath)

    sourceSubFolders= [f for f in os.listdir(sourceFolderPath) if os.path.isdir(os.path.join(sourceFolderPath, f))]
    replicaSubFolders= [f for f in os.listdir(replicaFolderPath) if os.path.isdir(os.path.join(replicaFolderPath, f))]
    
    for sourceSubFolders in sourceSubFolders:

        sourceSubFoldersPath=os.path.join(sourceFolderPath, sourceSubFolders)
        replicaSubFoldersPath=os.path.join(replicaFolderPath, sourceSubFolders)
        
        if sourceSubFolders not in replicaSubFolders:
            createFolder(replicaSubFoldersPath)

        folders(sourceSubFoldersPath, replicaSubFoldersPath)

    for replicaSubFolders in replicaSubFolders:
        replicaSubFoldersPath=os.path.join(replicaFolderPath, replicaSubFolders)
        if replicaSubFolders not in sourceSubFolders:
            deleteFolder(replicaSubFoldersPath)




    ##for replicaFile in replicaFile:
    ##    replicaFilePath=os.path.join(replicaFolderPath, replicaFile)
    ####    if replicaFile not in sourceFile:
    ####        deleteFile(replicaFilePath)
##  FAZER APAGADOR DE FILES
##

if __name__ == '__main__':
    sourceFolderPath = sys.argv[1]
    replicaFolderPath = sys.argv[2]
    sync_interval = int(sys.argv[3])
    log_filepath = sys.argv[4]

    logging.getLogger().handlers[0].baseFilename = log_filepath

    while True:
        folders(sourceFolderPath, replicaFolderPath)
        time.sleep(sync_interval)