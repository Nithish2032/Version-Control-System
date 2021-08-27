import click,difflib
import sys
from .commiting import *
import itertools

def printLine(columns,color):
    for _ in range(columns):
        click.secho("-",nl=False,fg=color,blink=True,bold=True)

def printTextOfSize(text,size,color):
    if text:
        click.secho(text,nl=False,fg=color,blink=True,bold=True)
        click.secho(" "*(size-len(text)),nl=False)
    else:
        click.secho(" "*size,nl=False)    
  
def simplediff(filename,tag1,tag2,color1,color2,border):
 
    hash1,branch1 = getHashAndBranch(tag1)
    hash2,branch2 = getHashAndBranch(tag2)

    file1 = f"{branchesPath}/{branch1}/{hash1}/{filename}"
    file2 = f"{branchesPath}/{branch2}/{hash2}/{filename}"

    if not (os.path.exists(file1) or os.path.exists(file2)):
        click.secho("Invalid Command")
        return

    screen = os.get_terminal_size()
    columns = screen.columns
    readTextSize = int((columns-8)/2)

    print()
    printLine(columns,border)
    print()

    with open(file1,"r") as f1:    
         with open(file2,"r") as f2:
              f1_List = f1.read().rstrip().split("\n")
              f2_List = f2.read().rstrip().split("\n")

    for text1,text2 in itertools.zip_longest(f1_List,f2_List):

          printTextOfSize(text1,readTextSize-2,color1) 
          print("    ",end="")
          printTextOfSize(text2,readTextSize,color2)
          print("  ")
    print()
    printLine(columns,border)

@click.command("diff")
@click.argument("filename",type=click.STRING)
@click.argument("tag1",type=click.STRING)
@click.argument("tag2",type=click.STRING)
@click.argument("color1",default="white")
@click.argument("color2",default="white")
@click.argument("border",default="white")
def diff(filename,tag1,tag2,color1,color2,border):
    """ compares two files side by side"""
    try:
      simplediff(filename,tag1,tag2,color1,color2,border)
    except:
      click.secho("Error occured.Could be because of the color you chose",fg="red")  
    return

@click.command("compare")
@click.argument("filename")
@click.argument("tag1")
@click.argument("tag2")
@click.argument("samecolor",default="green")
@click.argument("diffcolor",default="red")
@click.argument("border",default="white")        
def compare(filename,tag1,tag2,samecolor,diffcolor,border):
    """ Shows same lines in one color and different lines in another color."""

    hash1,branch1 = getHashAndBranch(tag1)
    hash2,branch2 = getHashAndBranch(tag2)

    file1 = f"{branchesPath}/{branch1}/{hash1}/{filename}"
    file2 = f"{branchesPath}/{branch2}/{hash2}/{filename}"

    if not (os.path.exists(file1) or os.path.exists(file2)):
        click.secho("Invalid Command")
        return

    screen = os.get_terminal_size()
    columns = screen.columns
    readTextSize = int((columns-8)/2)

    print()
    printLine(columns,border)
    print()

    with open(file1,"r") as f1:    
         with open(file2,"r") as f2:
              f1_List = f1.read().rstrip().split("\n")
              f2_List = f2.read().rstrip().split("\n")

    for text1,text2 in itertools.zip_longest(f1_List,f2_List):

          if text1 == text2:
             color = samecolor
          else:
             color = diffcolor  

          printTextOfSize(text1,readTextSize-2,color) 
          print("    ",end="")
          printTextOfSize(text2,readTextSize,color)
          print("  ")
    print()
    printLine(columns,border)

























