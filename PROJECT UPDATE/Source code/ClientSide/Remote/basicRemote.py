import click,socket,pickle,threading,time,sys,os

#GLOBAL VARIABLES
dirName = "vcs.ignore"
dataPath =f"{dirName}/data" 
userDataPath =f"{dataPath}/userData.object"
repoDataPath =f"{dataPath}/repoData.object"
commitLogPath =f"{dataPath}/commit.log"
treePath =f"{dataPath}/workingTree.object"
originDataPath =f"{dataPath}/originData.object"
branchesPath = f"{dirName}/branches"

IP = socket.gethostbyname(socket.gethostname())
PORT = 9998


def pickleLoad(objPath):
    with open(objPath,"rb+") as fh:
         return pickle.load(fh)
             
def pickleDump(obj,objPath):
    with open(objPath,"wb+") as fh:
         pickle.dump(obj,fh)

def connectToServer():
    try:
       clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       clientSocket.connect((IP,PORT))
    except:
       click.secho("Check your internet and try again.",fg="red")
       sys.exit()   
    
    return clientSocket
    
def getAccountDetails():
    account = {}
    click.secho("\n ENTER DETAILS \n",bold=True,blink=True,bg="blue")
    account["firstName"] = input("Enter your first name :")
    account["lastName"] = input("Enter your last name :")
    account["email"] = input("Enter your email id :")
    account["username"] = input("Set your username :")

    while True:
        password = input("Enter password :")
        confirmPassword = input("Confirm password :")

        if password == confirmPassword:
            account["password"] =password
            return account
        click.secho("Passwords didnt match.Try again.",fg="red")    

@click.command("createAccount")
def createAccount():
    """ You can create account with this command ."""

    clientSocket = connectToServer()
    account = getAccountDetails()

    PACKET = {"CMD":"CREATE_ACCOUNT"} 
    PACKET["account"]=account

    serializedAccount = pickle.dumps(PACKET)

    clientSocket.send(serializedAccount)

    msg = clientSocket.recv(1024).decode()

    if msg == "OK":
        click.secho("Account successfully created.",fg="green")
    elif msg == "EMAIL_EXISTS":
        click.secho("Account already exists with this email.", fg="red")
    elif msg == "UNAME_EXISTS":
        click.secho("username is taken.Try again.",fg="red")

def authenticate():

    if os.path.exists(userDataPath):
        userDataObj = pickleLoad(userDataPath)
        username = userDataObj.uname
        password = userDataObj.password

        if not password:
            username = input("\nEnter your username :")
            password = input("Enter your password :")

        userDataObj.uname = username
        userDataObj.password = password
        pickleDump(userDataObj,userDataPath)

    else:    
        username = input("\nEnter your username :")
        password = input("Enter your password :")

    userData = {}
    userData["username"] = username
    userData["password"] = password

    return userData
    
@click.command("mkrrep")
@click.argument("name",default="")
@click.option("--access","-a",default="public")
def makeRemoteRepo(name,access):
    """ You can make a new repository in the server ."""
    clientSocket = connectToServer()

    PACKET= {"CMD":"NEW_REPO"}
    PACKET["repoName"] = name
    PACKET["access"] = access
    PACKET["userData"] = authenticate()

    SERIALIZED_PACKET = pickle.dumps(PACKET)

    clientSocket.send(SERIALIZED_PACKET)

    msg = clientSocket.recv(1024).decode()

    if msg == "NOT_USER":
        click.secho("You are not a user.",fg="red")
    elif msg == "OK":
        click.secho("Repository successfully created.",fg="green")
    elif msg == "EXISTS":
        click.secho("Repository already exists in the server .",fg="blue") 
    elif msg == "WRONG_PASSWORD":
        click.secho("Incorrect password.",fg="red")       
    else:
        click.secho("Error ocurred.Try again",fg="red")
        
    clientSocket.close()            
    sys.exit()

if __name__=="__main__":
   pass





















