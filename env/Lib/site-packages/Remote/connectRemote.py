from .basicRemote import *

def checkValidPermissions(perm):

    if len(perm)==3 and perm[0] in ["-","R"] and perm[1] in ["-","W"] and perm[2] in ["-","A"]:
        return True
    click.secho("Invalid permissions.Try again.",fg="red")
    return False

def getCurrentRepoName():

    if not os.path.exists(repoDataPath):
        print(repoDataPath)
        click.secho("Current path does not have any repository.",fg="red")
        sys.exit()

    repoDataObj = pickleLoad(repoDataPath)

    return repoDataObj.repName

def addDevOne(clientSocket,PACKET,name,permissions):

    PACKET["CMD"] = "ADD_DEV_ONE"
    
    if not checkValidPermissions(permissions):
        sys.exit()
    
    PACKET["dev"] = { name : permissions }
    
    SERIALIZED_PACKET = pickle.dumps(PACKET)
    
    clientSocket.send(SERIALIZED_PACKET)
    
    msg = clientSocket.recv(1024).decode()

    if msg == "OK":
        click.secho("Developer successfully added to the repository.",fg="green")
    elif msg == "NOT_USER":
        click.secho("Developer does not exist.",fg="red")
    elif msg == "NO_ACCOUNT":
        click.secho("You do not have an account.",fg="red")
    elif msg == "NO_REPO":
        click.secho("Repository does not exist.",fg="red")
    elif msg == "WRONG_PASSWORD":
        click.secho("Incorrect password.",fg="red")        
    else:
        click.secho("Invalid operation",fg="red")    

def addDevMul(clientSocket,PACKET):
    
    PACKET["CMD"] = "ADD_DEV_MUL"
    SERIALIZED_PACKET = pickle.dumps(PACKET) 
    clientSocket.send(SERIALIZED_PACKET)

    msg = clientSocket.recv(1024).decode()

    if msg == "OK":
        click.secho("\n ENTER DEVELOPERS WITH PERMISSIONS \n",blink=True,bold=True,bg="blue")
    elif msg == "NO_REPO":
        click.secho("Invalid repository.",fg="red")
        sys.exit()
    elif msg == "WRONG_PASSWORD":
        click.secho("Invalid repository.",fg="red")
        sys.exit()
    elif msg == "NO_ACCOUNT":
        click.secho("You do not have an account.",fg="red")
        sys.exit()            
    else:
        click.secho("Invalid operation.Try again.",fg="red")
        sys.exit()           

    while True:        
        inp = input().split(" ")

        if not inp:
            click.secho("Invalid operation.Try agian.",fg="red")
 
        if inp[0] == "DONE!":
            sys.exit()


        if len(inp) == 2 and checkValidPermissions(inp[1]):

            DEV = { inp[0] : inp[1] }
            SERIALIZED_DEV = pickle.dumps(DEV)
            clientSocket.send(SERIALIZED_DEV)

            msg = clientSocket.recv(1024).decode()

            if msg == "OK":
                click.secho("Developer successfully added.",fg="green")
            elif msg == "NOT_USER":
                click.secho("Invalid user.",fg="red")               
            else:
                click.secho("Invalid operation.Try again",fg="red")  

@click.command("addDev")
@click.argument("repo",default=".")
@click.argument("name",default="")
@click.argument("permissions",default="")
def addDevs(repo,name,permissions):
    """ Add developers to your remote repository with this command.
        (nit addDev devname permission) for adding one developer.
        (nit addDev) for adding multiple developers.
        permissions should be in RWA format.
        You can user - for not giving that permission. eg: RW- """
    #print("before clientSocket") 
    clientSocket = connectToServer()
    #print("after connectToServer")

    PACKET = {}   

    if repo == ".":
        #print("inside repo .")
        repo = getCurrentRepoName()
        #print("after repo .")    

    PACKET["repo"] = repo
    PACKET["userData"] = authenticate()
    
    #print(f" name : {name} and permissions : {permissions}") 

    if name and permissions: 
        #print("in side add devs name and permissions")       
        addDevOne(clientSocket,PACKET,name,permissions)
    
    elif not name and not permissions:
        #print("in side add devs not name and not permissions")
        addDevMul(clientSocket,PACKET)

    else:
       click.secho("Invalid operation",fg="red")    

@click.command("showDevs")
@click.argument("repo",default=".")
def showDevs(repo):
    """ Shows all the developers that are added to your remote repository."""
    clientSocket = connectToServer()    
    
    if repo == ".":
        repo = getCurrentRepoName()       
    
    userData = authenticate()
        
    PACKET = { "CMD" : "SHOW_DEVS" }
    PACKET["repo"] = repo
    PACKET["userData"] = userData  

    SERIALIZED_PACKET = pickle.dumps(PACKET)    
    clientSocket.send(SERIALIZED_PACKET) 
               
    msg = clientSocket.recv(1024).decode()    

    if msg == "OK":
        pass
    elif msg == "NO_REPO":
        click.secho("Repository does not exist.",fg="red")
        sys.exit()
    elif msg == "NO_ACCOUNT":
        click.secho("You do not have an account.",fg="red")
        sys.exit()
    elif msg == "WRONG_PASSWORD":
        click.secho("Incorrect password.",fg="red")
        sys.exit()    
    else:
       click.secho("Invalid operation.Try again.",fg="red")
       sys.exit()

    SERIALIZED_DEV = clientSocket.recv(4096)    
    DEV = pickle.loads(SERIALIZED_DEV)    
    
    if not DEV.items():
        click.secho(f"\nNo developer other than you working on this repository.\n",fg="blue")
        return

    click.secho(f" Developer  Permissions",bg="blue",blink=True,bold=True)
    for key,value in DEV.items():
        click.secho(f" {key} : {value} ")


    

              

                























