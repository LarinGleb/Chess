
from curses.ascii import US
import json

from regex import D

from __main__ import game

PATH_TO_JSON_TEMP = "TempUsers.json"

def ImportData(path = PATH_TO_JSON_TEMP):
    with open(path, "r") as TempUser:
        data = json.load(TempUser)
    return data

def GetGame(code):
    return ImportData("Online.json")["Games"][code]

def AddGame(Game):
    data = ImportData("Online.json")
    games = data["Games"]
    games[Game.code]["Users"] = Game.users
    games[Game.code]["Desk"] = Game.Board.desk
    data["Games"] = games
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

def GetStatus(idUser: str = "NoneIp"):

    Users = ImportData("Online.json")["Users"]

    for user, status in Users.items():
        if user == idUser:
            return status

    return "find"

def GetOpponent(idUser: str = "None"):
    Games = ImportData("Online.json")["Games"]

    for userone, usertwo in Games['Players'].values():
        if userone == idUser:
            return usertwo
        elif usertwo == idUser:
            return userone

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
    users = data["Users"]
    users[ip] = property
    data["Users"] = users

    SaveData(data, "Online.json")

def AddProperty(ip: str = "NoneId", property: str = "EmptyProperty", value: str = "None"):

    data = ImportData()    
    dataUser = data[ip]
    dataUser[property] = value
    data[ip] = dataUser
    SaveData(data)
    