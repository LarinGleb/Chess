
import sqlite3
import datetime

connection = sqlite3.connect("Users/DB/Users.db", check_same_thread=False)
cursor = connection.cursor()

def AddUser(Ip: str="0.0.0.0.0", User: str = "DefaultUser", Password: str="DefaultPassword", Gmail: str ="example@domen"):
    cursor.execute(f"""INSERT INTO Users (Name, Ip, email, CountGames, CountLosses, CountWins, DataRegister) VALUES ("{User}", "{Ip}", "{Gmail}", 0, 0, 0, "{datetime.datetime.today().strftime('%Y.%m.%d')}")""") #(Name, Ip, email, CountGames, CountLosses, CountWins, DataRegister)
    cursor.execute(f"""INSERT INTO Security VALUES ("{User}", "{Password}")""")
    connection.commit()

def UserDefined(Ip: str="0.0.0.0.0", User: str = "DefaultUser"):
    global cursor
    Ips = cursor.execute("SELECT Ip from Users").fetchall()
    Users = cursor.execute("SELECT name from Users").fetchall()
    print(Ips)
    return Ip in Ips or User in Users

def PasswordAccepted(User: str="DefaultName", Password:str="DefaultPassword"):
    global cursor
    if not UserDefined(User=User):
        return False

    return Password == cursor.execute(f"SELECT Password from Security WHERE name = {User}")


