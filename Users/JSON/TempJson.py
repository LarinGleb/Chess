
import json

from regex import D

PATH_TO_JSON_TEMP = "TempUsers.json"

def ImportData(path = PATH_TO_JSON_TEMP):
    with open(path, "r") as TempUser:
        data = json.load(TempUser)
    return data

def AddGame(Game):
    data = ImportData("Online.json")["Games"]
    
    data[Game.code] = Game.users

    SaveData(data, "Online.json")
    
def SaveData(data, PATH = PATH_TO_JSON_TEMP):
    with open(PATH, "w") as TempUser:
        json.dump(data, TempUser, indent=4)

def DeleteUser(idUser):
    data = ImportData()
    del data[idUser]
    SaveData(data)

def GetNameByIP(idUser: str = "NoneIp"):
    
    for user, info in ImportData().items():
        if info["ip"] == idUser:
            return user
    return ""

def GetPropertyUser(idUser: str = "NoneIp", property: str = "EmptyProperty"):
    return ImportData()[idUser][property]

def AddUser(idUser: str = "ip"):
    data = ImportData()
    data[idUser] = dict()
    SaveData(data)

def GetAllPossibleUsers(ipUser: str = "None"):
    possibleUsers = []
    statusUsers = ImportData('Online.json')["Users"]

    for user, status in statusUsers.items():
        if user != ipUser and status == "find":
            possibleUsers.append(user)
    return possibleUsers

def SetUserGame(ip: str = "NoneId", property: str = "None"):
    data = ImportData("Online.json")
    data["Users"][ip] = property
    
    SaveData(data, "Online.json")

def AddProperty(ip: str = "NoneId", property: str = "EmptyProperty", value: str = "None"):

    data = ImportData()    
    dataUser = data[ip]
    dataUser[property] = value
    data[ip] = dataUser
    SaveData(data)
    