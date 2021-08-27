import socket,pickle,sqlite3,threading,time,os,sys,shutil
from ServerClasses import *
from fileTransfer import *
import checksumdir

IP = socket.gethostbyname(socket.gethostname())
PORT = 9998

readLock = Lock()
writeLock = Lock()

def handler(conn):

        SERIALIZED_PACKET = conn.recv(4096)
        PACKET = pickle.loads(SERIALIZED_PACKET)

        print(f"PACKET : {PACKET}")

        cmd = PACKET["CMD"]

        if cmd == "CREATE_ACCOUNT": 
           createAccount(PACKET,conn)

        elif cmd == "NEW_REPO":
           makeNewRepo(PACKET,conn)

        elif cmd == "ADD_DEV_ONE":
           addDevOne(PACKET,conn)

        elif cmd == "ADD_DEV_MUL": 
           addDevMul(PACKET,conn)

        elif cmd == "SHOW_DEVS":
           showDevs(PACKET,conn)

        elif cmd == "PUSH_REPO":
           pushRepo(PACKET,conn)         
        conn.close()
                  
def main():
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((IP,PORT))
    print("Server started.")
    
    while True:
        serverSocket.listen(5)
        conn,addr = serverSocket.accept()

        print(f"Server connected to {addr}.")
        try :
            newThread = threading.Thread(target=handler,args=(conn,))
            newThread.start()
        except:
            pass    
        print(f"Client with {addr} starts in new thread.")

def connectToDB():
    print("Connected to database successfully.")
    dbConn = sqlite3.connect("database.db")
    cursor = dbConn.cursor()
    return cursor,dbConn

def pickleLoad(objPath):
    with open(objPath,"rb+") as fh:
         return pickle.load(fh)
             
def pickleDump(obj,objPath):
    with open(objPath,"wb+") as fh:
         pickle.dump(obj,fh)

def createAccount(PACKET,conn):

    account = PACKET["account"]

    firstName = account["firstName"]
    lastName = account["lastName"]
    email = account["email"]
    username = account["username"]
    password = account["password"]

    cursor,dbConn = connectToDB()

    query = """ SELECT 1 FROM USERS WHERE email = ? """
    result = cursor.execute(query,(email,)).fetchone()

    if result:
        conn.send("EMAIL_EXISTS".encode())
        return

    query = """ SELECT 1 FROM USERS WHERE username = ? """    
    result = cursor.execute(query,(username,)).fetchone()

    if result:
        conn.send("UNAME_EXISTS".encode())
        return

    curTime = time.ctime(time.time())

    query = """ INSERT INTO USERS VALUES(?,?,?,?,?,?) """
    cursor.execute(query,(username,firstName,lastName,email,password,curTime,))

    dbConn.commit()

    os.mkdir(f"Users/{username}")
    open(f"Users/{username}/notifications.log","w").close()
    open(f"Users/{username}/latestNotifs.log","w").close()
    
    conn.send("OK".encode())

    print("Account Successfully created")

def authenticate(conn,username,password):

    if not isUser(username):
        conn.send("NO_ACCOUNT")
        return False

    cursor,dbConn = connectToDB()
    query = """ SELECT PASSWORD FROM USERS WHERE USERNAME = ? """    
    result = cursor.execute(query,(username,)).fetchone()

    if result[0] != password:
        conn.send("WRONG_PASSWORD".encode())
        conn.close()
        return False

    return True    
   
def makeNewRepo(PACKET,conn):

    repoName = PACKET["repoName"] 
    access = PACKET["access"]
    userData = PACKET["userData"]
    username = userData["username"]
    password = userData["password"]
    
    if not authenticate(conn,username,password):
        return   

    repoPath = f"Users/{username}/{repoName}"

    if os.path.exists(repoPath) :
        conn.send("EXISTS".encode())
        return

    dirs = ["","/repoData","/pullReqsDir"]
    files = ["/pullReqs.log","/curPullReqs","/accessData.object"]

    for dir in dirs:
        os.mkdir(f"{repoPath}{dir}")

    for file in files:
        open(f"{repoPath}/repoData{file}","w").close()     

    accessDataPath = f"{repoPath}/repoData/accessData.object"
    accessDataObj = accessData(access)
    pickleDump(accessDataObj,accessDataPath)

    conn.send("OK".encode())       

def isUser(name):

    cursor,dbConn = connectToDB()
    query = """ SELECT 1 FROM USERS WHERE USERNAME = ? """
    result = cursor.execute(query,(name,)).fetchone()

    return result

def addDevOne(PACKET,conn):

    userData = PACKET["userData"]
    username = userData["username"]
    password = userData["password"] 
    repo = PACKET["repo"]
    devDict = PACKET["dev"]

    if not authenticate(conn,username,password):
        return
    
    repoPath = f"Users/{username}/{repo}"

    if not os.path.exists(repoPath):
       conn.send("NO_REPO".encode())
       return

    for dev in devDict.keys():
        if not isUser(dev):
           conn.send("NOT_USER".encode()) 
           return 

    accessDataPath = f"{repoPath}/repoData/accessData.object"
    
    readLock.acquire(accessDataPath)
    writeLock.acquire(accessDataPath)

    accessDataObj = pickleLoad(accessDataPath)
    accessDataObj.addDevelopers(devDict)
    pickleDump(accessDataObj,accessDataPath)

    readLock.release(accessDataPath)
    writeLock.release(accessDataPath)

    conn.send("OK".encode())

    return

def addDevMul(PACKET,conn):

    userData = PACKET["userData"]
    username = userData["username"]
    password = userData["password"]
    repo = PACKET["repo"]

    if not authenticate(conn,username,password):
        return    
    
    repoPath = f"Users/{username}/{repo}"

    if not os.path.exists(repoPath):
       conn.send("NO_REPO".encode())
       return    

    tempDevDict = {}

    conn.send("OK".encode())

    while True:
        SERIALIZED_DEV = conn.recv(1024)
        DEV = pickle.loads(SERIALIZED_DEV)

        if not DEV :
            conn.close()
            return

        for key,value in DEV.items():
            if not isUser(key):
               conn.send("NOT_USER".encode()) 
               return 
            tempDevDict[key]=value

        conn.send("OK".encode())

    accessDataPath = f"{repoPath}/repoData/accessData.object"    
    
    readLock.acquire(accessDataPath)
    writeLock.acquire(accessDataPath)
    
    accessDataObj = pickleLoad(accessDataPath)
    accessDataObj.addDevelopers(tempDevDict)     
    pickleDump(accessDataObj,accessDataPath)

    readLock.release(accessDataPath)
    writeLock.release(accessDataPath)  

def showDevs(PACKET,conn):
    
    userData = PACKET["userData"]
    username = userData["username"]
    password = userData["password"]

    repo = PACKET["repo"]

    if not authenticate(conn,username,password):
        sys.exit()
    
    accessDataPath = f"Users/{username}/{repo}/repoData/accessData.object"

    writeLock.acquire(accessDataPath)
    accessDataObj = pickleLoad(accessDataPath)
    writeLock.release(accessDataPath)

    SERIALIZED_DEV = pickle.dumps(accessDataObj.developers)

    conn.send("OK".encode())
    conn.send(SERIALIZED_DEV)

def copyAndOverwrite(src,dest):
    for file in os.listdir(src):
        if isBinary(file):
            with open(f"{src}/{file}","rb") as f1:
                f1_text = f1.read()
            with open(f"{dest}/{file}","wb") as f2:
                f2.write(f1_text)
        else:
            with open(f"{src}/{file}","r") as f1:
                f1_text = f1.read()
            with open(f"{dest}/{file}","w") as f2:
                f2.write(f1_text)
                   

def moveFolders(src,dest):
    for file in os.listdir(src):
        shutil.move(src,dest)

def getFirstPush(conn,path):
    recvFolder(conn,path)
    
    src = f"{path}/vcs.ignore/branches"
    dest = f"{path}"
    moveFolders(src,dest)
    src = f"{path}/vcs.ignore/data"
    dest = f"{path}/repoData"
    copyAndOverwrite(src,dest)



def pushRepo(PACKET,conn):
    print("inside pushRepo")
    userData = PACKET["userData"]
    username = userData["username"]
    password = userData["password"]
    repoName = PACKET["repo"]

    if not authenticate(conn,username,password):
        return

    repoPath = f"Users/{username}/{repoName}"

    if not os.path.exists(repoPath):
       conn.send("NO_REPO".encode()) 

    branchesPath = f"{repoPath}/branches"

    print(f" branchesPath : {branchesPath} ")
    if not os.path.exists(branchesPath):
       conn.send("FIRST_PUSH".encode())
       getFirstPush(conn,repoPath)      
       return

    conn.send("NEW_PUSH".encode())
   

if __name__=="__main__":
   main()


























































































































































































































































































































































