import click,shutil,checksumdir,time,sys
from .basic import *

def getHashAndBranch(tag):
    tempTreeObj = pickleLoad(treePath)
    tempNodeObj = tempTreeObj.myGraph[tag]
    return tempNodeObj.hashValue,tempNodeObj.branch

@click.command("getHash")
@click.argument("tag")
def getHash(tag):
    """ Gives you hash number of a certain tag. """   
    tempTreeObj = pickleLoad(treePath)
    tempNodeObj = tempTreeObj.myGraph[tag]
    click.secho(tempNodeObj.hashValue)    
                        
@click.command("getTag")
@click.argument("hash")                
def getTag(hash):
    """ Gives you tag of a certain hash number. """
    tempTreeObj = pickleLoad(treePath)    
    for tempNodeObj in tempTreeObj.myGraph.values():
        if tempNodeObj.hashValue == hash:
           click.secho(tempNodeObj.tag)
           return
    click.secho("Invalid hash",fg="red")       
             
def getTagValue(tagNumber):
    first,second,third = tagNumber[1:].split(".")
    tagValue = int(first+second+third)
    return tagValue

def getTagNumber(tagValue):
    tagStr = str(tagValue)

    if tagValue < 10 :
       newTagNumber = f"v0.0.{tagStr}"
    elif tagValue < 100:
        newTagNumber = f"v0.{tagStr[0]}.{tagStr[1]}"
    else:
        newTagNumber = f"v{tagStr[0]}.{tagStr[1]}.{tagStr[2]}"

    return newTagNumber    
        
def writeToLog(newTag,hashValue,curBranch,uname,email,timeCommited,commitMsgShort):
    with open(commitLogPath,"a") as fh:
        fh.write(f"commit {hashValue}    {newTag}\n")
        fh.write(f"branch : {curBranch}\n")
        fh.write(f"user : {uname}    {email}\n")
        fh.write(f"Time : {timeCommited}\n")
        fh.write(f"Message : {commitMsgShort}")

def nextTag(curTag):
    
    newTagValue = getTagValue(curTag) + 1
    newTagNumber = getTagNumber(newTagValue)
    return newTagNumber

def makeNewCommitFolder(curBranch,trackList):
    curCommitPath = f"{branchesPath}/{curBranch}/head"

    os.mkdir(curCommitPath)
    for file in trackList:
        shutil.copy(file,curCommitPath)        

    hashValue = checksumdir.dirhash(curCommitPath)
    newCommitPath = f"{branchesPath}/{curBranch}/{hashValue}" 

    for branch in os.listdir(branchesPath):
        for folder in os.listdir(f"{branchesPath}/{branch}"):
            
            if folder == hashValue:
                click.secho("Commit already exists.",fg="red")
                shutil.rmtree(curCommitPath,ignore_errors=True)
                sys.exit()

    os.rename(curCommitPath,newCommitPath)

    return hashValue,newCommitPath     

def writeCommitMsg(arg,newCommitPath):

    commitMsgLongPath = f"{newCommitPath}/commitMsgLong.txt"
    open(commitMsgLongPath,"w").close()
    if arg == "":
        click.edit(filename = commitMsgLongPath)
        with open(commitMsgLongPath,"r") as f1:
            commitMsgShort = f1.readline()
    else :
        commitMsgShort = arg

    return commitMsgShort       

def setNodeInTree(tag,hashValue,curBranch,uname,email,timeCommited,commitMsgShort):

    tempNodeObj = Node(tag,hashValue,curBranch,uname,email,timeCommited,commitMsgShort)

    if tag == "v0.0.1":
        myGraph = {tag:tempNodeObj}
        base = tag
        heads = {curBranch:tag}

        tempTreeObj = Tree(myGraph,base,heads)

    else :
        tempTreeObj = pickleLoad(treePath)
        heads = tempTreeObj.heads
        prevHeadTag = heads[curBranch]

        tempTreeObj.setNodeInTree(tag,tempNodeObj)
        tempTreeObj.setEdge(prevHeadTag,tag)
        heads[curBranch]=tag
        tempTreeObj.heads = heads

    pickleDump(tempTreeObj,treePath)

@click.command("commit")
@click.argument('arg',default="")
def commit(arg):
    """ It takes a snapshot of the current version of your repository."""
    repoDataObj = pickleLoad(repoDataPath)
    trackList = repoDataObj.trackList
    curBranch = repoDataObj.curBranch
    curTag = repoDataObj.curTag

    hashValue,newCommitPath=makeNewCommitFolder(curBranch,trackList)   
    
    newTag = nextTag(curTag)
    repoDataObj.curTag = newTag
    pickleDump(repoDataObj,repoDataPath)

    commitMsgShort = writeCommitMsg(arg,newCommitPath)
    
    timeCommited = time.ctime(time.time())

    userDataObj = pickleLoad(userDataPath)
    uname = userDataObj.uname
    email = userDataObj.email

    writeToLog(newTag,hashValue,curBranch,uname,email,timeCommited,commitMsgShort)

    setNodeInTree(newTag,hashValue,curBranch,uname,email,timeCommited,commitMsgShort)

def tailRead(fh,n):
    return fh.readlines()[-n:]

def headRead(fh,n):
    return fh.readlines()[:n]

@click.command("history")
#@click.option("--date","-d",default="")
@click.option("--tail","-t",default=-1,help="shows recent commits")
@click.option("--head","-h",default=-1,help="shows old commits")
def history(tail,head):
    """ You can view your commit history with this command. """
    click.secho()
    with open(commitLogPath,"r") as f3:

        if tail == -1 and head == -1:           
            for line in f3.readlines():
                click.secho(line,nl=False)

        if tail > 0:
            lines = tailRead(f3,tail*6)
            for line in lines:
                click.secho(line,nl=False)

        if head > 0:
           lines = headRead(f3,head*5)
           for line in lines:
                click.secho(line,nl=False)
    click.secho()                     
    
@click.command("revert")
@click.argument("arg")            
def revert(arg):
    """ You can go back to any commit you have made earlier with this command."""
    if len(arg)==32:
        tag = getTag(arg)
    elif len(arg)==6:
        tag = arg

    hashValue,branch = getHashAndBranch(arg)    
    dest = os.getcwd()
    src = f"{branchesPath}/{branch}/{hashValue}"

    for file in os.listdir(src):
        if file == "commitMsgLong.txt":
            continue
        shutil.copyfile(f"{src}/{file}",f"{dest}/{file}")



























