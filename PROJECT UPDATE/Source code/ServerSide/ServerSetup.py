import sqlite3,os

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
  setupServer() 

























