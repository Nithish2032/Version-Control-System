import time
class accessData:
    def __init__(self,access="public",developers={}):
        self.access = access
        self.developers = developers

    def modifyAccess(self,arg):

        if arg == "private":
            self.access = "private"
        elif arg == "public":
            self.access = "public"
        else:
            return

    def addDevelopers(self,myDict):
        print("in side class method")
        for key,value in myDict.items():
            self.developers[key] = value
        return  

class Lock:
    def __init__(self):
        self.locked = []                       
    
    def acquire(self,path):
        print("In class acquire function")
        while True:
            print("running in acquire lock")
            time.sleep(0.5)
            print(self.locked)
            if path not in self.locked:
                print("inside path not in")
                break
        print("before locked append")        
        self.locked.append(path)
        print("after locked append")
        return    

    def release(self,path):
        self.locked.remove(path)
        return   



















