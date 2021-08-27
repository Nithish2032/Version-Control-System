import sqlite3,os,subprocess

def installReqs():
    commands = [ ["sudo","apt","update"],
                 ["sudo","apt","install","python3-pip"],
                 ["pip","install","click"],
                 ["pip","install","checksumdir"] ]
    
    for command in commands:
        try:
          output = subprocess.run(command,capture_output=True)
          print(f"{output}\n\n")
        except:
          print(f"\n\nEXECPTION AT {command}\n\n")
          continue
           

def setupServer():
    conn = sqlite3.connect("database.db")
    print(f"database.db created successfully")

    conn.execute('''CREATE TABLE USERS
         (USERNAME TEXT PRIMARY KEY,
          FIRSTNAME TEXT,
          LASTNAME  TEXT,
          EMAIL TEXT,
          PASSWORD TEXT,
          TIME_CREATED TEXT);
             ''')

    print(f"Table created successfully")
    os.mkdir("Users")
    print(f"Users directory created successfully")

if __name__=="__main__":
  #installReqs()
  setupServer() 

























