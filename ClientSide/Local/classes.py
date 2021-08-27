class userData:
    def __init__(self,uname=None,email=None,password=None):
        self.uname = uname
        self.email = email
        self.password = password

class repoData:
    def __init__(self,repName,trackList=[],curBranch="master",curTag="0.0.0"):
        self.repName = repName
        self.trackList = trackList
        self.curBranch = curBranch
        self.curTag = curTag           

class originData:
    def __init__(self,aname,email,desc,timeCreated):
        self.aname = aname
        self.email = email
        self.desc = desc
        self.timeCreated = timeCreated
       
class Node:
   def __init__(self,tag,hashValue,branch,uname,email,timeCommited,commitMsgShort):
       self.tag = tag
       self.hashValue = hashValue
       self.branch = branch
       self.uname = uname
       self.email = email
       self.timeCommited = timeCommited
       self.commitMsgShort = commitMsgShort
       self.prev = []
       self.next = []

   def addNext(self,nextTag):
       self.next.append(nextTag)

   def addPrev(self,prevTag):
       self.prev.append(prevTag)        

class Tree:
    def __init__(self,myGraph,base,heads):
        self.myGraph = myGraph
        self.base = base
        self.heads = heads

    def setNodeInTree(self,tag,NodeObj):
        self.myGraph[tag] = NodeObj
    
    def setEdge(self,oldNodeTag,newNodeTag):
        oldNode = self.myGraph[oldNodeTag]
        newNode = self.myGraph[newNodeTag]

        oldNode.addNext(newNodeTag)
        newNode.addPrev(oldNodeTag)

    def getObjFromTag(self,tag):
        return self.myGraph[tag]

    def printTree(self):
        pass  


            

                













               
