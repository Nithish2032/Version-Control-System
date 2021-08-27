from .connectRemote import *
from .fileTransfer import *

def sendFirstPush(clientSocket):
    sendFolder(clientSocket,dirName)
    return


@click.command("push")
def pushRepo():
    """ Upload your repository to server with this command."""
    clientSocket = connectToServer()

    PACKET = { "CMD" : "PUSH_REPO" }
    PACKET["userData"] = authenticate()
    #print("after authenticate")
    PACKET["repo"] = getCurrentRepoName()
    #print("after repo")
    SERIALIZED_PACKET = pickle.dumps(PACKET)

    clientSocket.send(SERIALIZED_PACKET)

    #print("after clientSocket")
    msg = clientSocket.recv(1024).decode()
    # print(f"msg is {msg}")

    if msg == "NO_ACCOUNT":
        click.secho("You dont have an account.",fg="red")
    elif msg == "NO_REPO":
        click.secho("Repository does not exist in the server.",fg="red")
    elif msg == "FIRST_PUSH":
        #print("inside FIRST_PUSH")
        sendFirstPush(clientSocket)
    elif msg == "NEW_PUSH":
        pass
    elif msg == "WRONG_PASSWORD":
       click.secho("Incorrect password.Try again.",fg="red")
    else:
       click.secho("Invalid operation",fg="red")                



















