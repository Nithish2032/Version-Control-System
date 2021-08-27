import click,os
from .basic import *

@click.command("mkbr")
@click.argument("branchname")
def makeBranch(branchname):
    """ You can make a new branch with this command. """
    mkbr(branchname) 

@click.command("chbr")
@click.argument("branchname")
def changeBranch(branchname):
    """ You can change your current working branch with this command."""
    chbr(branchname)    

def chbr(branchname):

    if not os.path.exists(f"{branchesPath}/{branchname}"):
        click.secho("Branch does not exits.",fg="red")
        return
    repoDataObj = pickleLoad(repoDataPath)
    repoDataObj.curBranch = branchname
    pickleDump(repoDataObj,repoDataPath)

def mkbr(branchname):
    newBranchPath = f"{branchesPath}/{branchname}"
    if os.path.exists(newBranchPath):
       click.secho("Branch already exists.",fg="red")
       return
    os.mkdir(newBranchPath)

    repoDataObj = pickleLoad(repoDataPath)
    curBranch = repoDataObj.curBranch

    treeObj = pickleLoad(treePath)
    heads = treeObj.heads

    curBranchHead = heads[curBranch]
    heads[branchname]=curBranchHead
    treeObj.heads=heads

    pickleDump(treeObj,treePath)

    chbr(branchname)

@click.command("branches")
def showBranches():
    """ Shows all the branches that are present in the repository."""
    click.secho("\nBranches : ",nl=False)
    for dir in os.listdir(branchesPath):
        click.secho(f"{dir} ",nl=False)
    click.secho()           



    
            



















