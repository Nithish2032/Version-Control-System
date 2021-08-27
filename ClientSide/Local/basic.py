import click,os,time,pickle
from .classes import *

#GLOBAL VARIABLES
dirName = "vcs.ignore"
dataPath =f"{dirName}/data" 
userDataPath =f"{dataPath}/userData.object"
repoDataPath =f"{dataPath}/repoData.object"
commitLogPath =f"{dataPath}/commit.log"
treePath =f"{dataPath}/workingTree.object"
originDataPath =f"{dataPath}/originData.object"
branchesPath = f"{dirName}/branches"
    
def pickleLoad(objPath):
    with open(objPath,"rb+") as fh:
         return pickle.load(fh)
             
def pickleDump(obj,objPath):
    with open(objPath,"wb+") as fh:
         pickle.dump(obj,fh)

def checkFile(filePath):
    if filePath == dirName or not os.path.exists(filePath):
        click.secho("Invalid File",fg="red")
        return False
    return True    


@click.command("init")
def init():
    """ Initializes the repository."""
    if os.path.exists(dirName):                          
        wrng_msg = "Repository already initialized."
        click.secho(wrng_msg,fg="red")
        return 

    repName = input("Repository Name :")
    aName = input("Author Name :")
    aEmail = input("Author Email :")
    desc = input("Description :")
    timeCreated = time.ctime(time.time())

    dirsToCreate = ["","/data","/branches","/branches/master"]

    for dir in dirsToCreate:
        fn= f"{dirName}{dir}"
        os.mkdir(fn)                                    
        os.popen('attrib +h ' + fn)

    repoDataObj = repoData(repName) 
    pickleDump(repoDataObj,repoDataPath)    

    originDataObj = originData(aName,aEmail,desc,timeCreated)                                   
    pickleDump(originDataObj,originDataPath)

    userDataObj = userData(aName,aEmail)
    pickleDump(userDataObj,userDataPath)

    open(commitLogPath,"w").close()
    open(treePath,"w").close()

@click.command("track")
@click.argument("arg",default="mul")
def track(arg):
    """ Add files to you want track using this command.
        nit track * for tracking every file in the current path.
        nit track filename for tracking one file.
        nit track for adding multiple files (type DONE! when your are done)."""
    tempTrackList = []
    if arg=="*":
        for file in os.listdir():
            if file==dirName:
                continue
            tempTrackList.append(file)               
        
    elif arg=="mul":
         while True:
            inp = input()
            if inp == "DONE!":
                break
            if checkFile(inp):  
               tempTrackList.append(inp)    
        
    else: 
       if not checkFile(arg): 
          return 
          
       tempTrackList.append(arg)    
    
    repoDataObj = pickleLoad(repoDataPath)

    for file in tempTrackList:
        if file not in repoDataObj.trackList:
           repoDataObj.trackList.append(file)
    
    pickleDump(repoDataObj,repoDataPath)

@click.command("ignore")
@click.argument('arg',default="mul")
def ignore(arg):
    """ Ignore the files that you dont want to track with this command."""
    tempIgnoreList = []
    if arg=="*":
        for file in os.listdir():
            if file==dirName:
                continue
            tempIgnoreList.append(file)    
        
    elif arg =="mul":
         while True:
            inp = input()
            if inp == "DONE!":
                break
            if checkFile(inp):  
               tempIgnoreList.append(inp)    
        
    else: 
       if not checkFile(arg): 
          return 
          
       tempIgnoreList.append(arg)    

    repoDataObj = pickleLoad(repoDataPath)

    for file in tempIgnoreList:
        if file in repoDataObj.trackList:
           repoDataObj.trackList.remove(file)

    pickleDump(repoDataObj,repoDataPath)

@click.command("status")    
def status():
    """ Shows the status of your repository """
    repoDataObj = pickleLoad(repoDataPath)
    curBranch = repoDataObj.curBranch
    trackList = repoDataObj.trackList
    
    click.secho("\nOn branch ",nl=False)
    click.secho(curBranch,nl=False,fg="blue")
    click.secho(".\n")

    if len(trackList)==0:
        click.secho("Tracking : None")
    else:
       click.secho("Tracking : ",nl=False) 
       for file in trackList:
           click.secho(f"{file} ",nl=False)
       click.secho()      

       

      

             













