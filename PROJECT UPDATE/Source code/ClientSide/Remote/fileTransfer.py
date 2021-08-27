import os,math,pickle

BUFFER_SIZE = 1024

def isBinary(fileName):
    if ".object" in fileName:
       return True
    return False    

def getFileSize(filePath):

    if isBinary(filePath):
       fh = open(filePath,"rb")
    else:   
       fh = open(filePath,"r")
       
    return len(fh.read())


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
        sendFile(conn,curPath,file[0],file[1])

def sendFile(conn,path,fileName,fileSize):

    filePath = os.path.join(path,fileName)

    passes = math.ceil(fileSize/BUFFER_SIZE)

    if isBinary(fileName):
       with open(filePath,"rb") as fh:
        for passNo in range(1,passes+1):
            readText = fh.read(BUFFER_SIZE)
            #print(f"readText: {readText}")
            conn.send(readText) 
      
    else:
      with open(filePath,"r") as fh:
        for passNo in range(1,passes+1):
            readText = fh.read(BUFFER_SIZE)
            conn.send(readText.encode())       


def recvFolder(conn,path):
    SERIALIZED_TREE = conn.recv(4096)
    dirTree = pickle.loads(SERIALIZED_TREE)
    myDirTree = dirTree[1]

    print(f"\n\n\n {myDirTree} \n\n\n")

    rootDirPath = os.path.join(path,dirTree[0]) 
    os.mkdir(rootDirPath)

    for row in myDirTree:
        lineProcessRecv(conn,rootDirPath,row)    

def lineProcessRecv(conn,path,row):
    curPath = os.path.join(path,row[0])

    for directory in row[1]:
       dirPath = os.path.join(curPath,directory)
       os.mkdir(dirPath)
    
    for file in row[2]:
      recvFile(conn,curPath,file[0],file[1])
           
def recvFile(conn,path,fileName,fileSize):

    filePath = os.path.join(path,fileName)

    passes = math.ceil(fileSize/BUFFER_SIZE)

    if isBinary(fileName):
       print(f"{fileName} is is binary")

       with open(filePath,"ab") as fh:
          for passNo in range(1,passes+1):
              print(f"passNo : {passNo}")
              if passNo == passes:
                 newBufferSize = fileSize - (passNo-1)*BUFFER_SIZE
                 writeText = conn.recv(newBufferSize)   
              else:
                 writeText = conn.recv(BUFFER_SIZE)
              print(writeText)   

              fh.write(writeText)

    else:

        with open(filePath,"a") as fh:
            for passNo in range(1,passes+1):
                if passNo == passes:
                   newBufferSize = fileSize - (passNo-1)*BUFFER_SIZE
                   writeText = conn.recv(newBufferSize).decode()   
                else:
                   writeText = conn.recv(BUFFER_SIZE).decode()

                fh.write(writeText)



                 
       










