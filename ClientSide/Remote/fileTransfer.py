import os,math,pickle

BUFFER_SIZE = 1024  

def getFileSize(filePath):

    fileSize = os.stat(filePath).st_size 
       
    return fileSize

def extractDirTree(path):

    myDirTree = []
    rootBaseName = os.path.basename(path)

    for root,dirs,files in os.walk(path):
        myFileList = []
        for file in files:
           filePath = os.path.join(root,file)
           fileSize = getFileSize(filePath)
           myFileList.append((file,fileSize))   
        
        relativePath = os.path.relpath(root,path)      
        myDirTree.append([relativePath,dirs,myFileList])

    dirTree = [rootBaseName,myDirTree]    
    return dirTree    

def sendFolder(conn,path):
    dirTree = extractDirTree(path)
    SERIALIZED_TREE = pickle.dumps(dirTree)
    conn.send(SERIALIZED_TREE)

    myDirTree = dirTree[1]

    for row in myDirTree:
       lineProcessSend(conn,path,row)
  
def lineProcessSend(conn,path,row):
    curPath = os.path.join(path,row[0])

    for file in row[2]:
        sendMyFile(conn,curPath,file[0],file[1])

def sendMyFile(conn,path,fileName,fileSize):

    filePath = os.path.join(path,fileName)

    passes = math.ceil(fileSize/BUFFER_SIZE)

    with open(filePath,"rb") as fh:
       for passNo in range(1,passes+1):
           readText = fh.read(BUFFER_SIZE)
           conn.send(readText)
      
def sendFile(conn,path):
    dirPath,fileName = os.path.split(path)
    fileSize = getFileSize(path)

    conn.send(f"{fileName} {fileSize}".encode())
    sendMyFile(conn,dirPath,fileName,fileSize)

def recvFolder(conn,path):

    SERIALIZED_TREE = conn.recv(4096)

    dirTree = pickle.loads(SERIALIZED_TREE)
    myDirTree = dirTree[1]
    rootDirPath = f"{path}/{dirTree[0]}" 
    os.mkdir(rootDirPath)

    for row in myDirTree:
        lineProcessRecv(conn,rootDirPath,row)    

def lineProcessRecv(conn,path,row):
    curPath = os.path.join(path,row[0])

    for directory in row[1]:
       dirPath = os.path.join(curPath,directory)
       os.mkdir(dirPath)
    
    for file in row[2]:
      recvMyFile(conn,curPath,file[0],file[1])
           
def recvMyFile(conn,path,fileName,fileSize):

    filePath = os.path.join(path,fileName)
    passes = math.ceil(fileSize/BUFFER_SIZE)

    with open(filePath,"ab") as fh:
       for passNo in range(1,passes+1):

          if passNo == passes:
             newBufferSize = fileSize - (passNo-1)*BUFFER_SIZE
             writeText = conn.recv(newBufferSize)   
          else:
             writeText = conn.recv(BUFFER_SIZE)

          fh.write(writeText)

def recvFile(conn,path):
    fileInfo = conn.recv(256).decode().split()
    fileName,fileSize = fileInfo[0],int(fileInfo[1]) 
    recvMyFile(conn,path,fileName,fileSize)         
    
def sendDirs(conn,dirList=[],fileList=[]):
    dirs = len(dirList)
    files = len(fileList)

    if not files and not dirs:
      return
    
    PACKET = {"files":files,"dirs":dirs}
    SERIALIZED_PACKET = pickle.dumps(PACKET)
    conn.send(SERIALIZED_PACKET)

    for DIR in dirList:
        sendFolder(conn,DIR)
        msg = conn.recv(64).decode()
        if msg == "OK":
           continue
        else:
           return   

    for FILE in fileList:
        sendFile(conn,FILE)
        msg = conn.recv(64).decode()
        if msg == "OK":
           continue
        else:
           return      
    
def recvDirs(conn,path):
    SERIALIZED_PACKET = conn.recv(4096)
    PACKET = pickle.loads(SERIALIZED_PACKET)

    files = PACKET["files"]
    dirs = PACKET["dirs"]

    for _ in range(dirs):
        recvFolder(conn,path)
        conn.send("OK".encode())
    for _ in range(files):
        recvFile(conn,path)
        conn.send("Ok".encode())    


                 
       

