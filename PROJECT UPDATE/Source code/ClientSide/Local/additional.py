import click,difflib
import sys
from .commiting import *

def simplediff(filename,tag1,tag2):
 
    hash1,branch1 = getHashAndBranch(tag1)
    hash2,branch2 = getHashAndBranch(tag2)

    file1 = f"{branchesPath}/{branch1}/{hash1}/{filename}"
    file2 = f"{branchesPath}/{branch2}/{hash2}/{filename}"

    if not (os.path.exists(file1) or os.path.exists(file2)):
        click.secho("Invalid Command")
        return

    with open(file1,"r") as f1:
        f1_text = f1.read()
    with open(file2,"r") as f2:
        f2_text = f2.read()
    
    d = difflib.Differ()
    result = list(d.compare(f1_text,f2_text))
    sys.stdout.writelines(result)

@click.command("diff")
@click.argument("filename",type=click.STRING)
@click.argument("tag1",type=click.STRING)
@click.argument("tag2",type=click.STRING)
# @click.option("--detailed","-d",default=False)

def diff(filename,tag1,tag2):
    """ compares two files """
    simplediff(filename,tag1,tag2)
    return

        
























