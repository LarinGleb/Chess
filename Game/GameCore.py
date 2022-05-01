
from .Chess import Board
import random

def GenerateCode(Users):
    user_one, user_two = Users
    return str(id(user_one)) + str(id(user_two))

class Game():
    def __init__(self, users, Board = Board()):
        self.code = GenerateCode(users)
        self.Board = Board
        self.users = users
        self.SetColors()

    

    def InverseColor(self, color):
        return 1 if color == -1 else -1

    def SetColors(self):
        self.Userscolor = {}
        self.colorUsers = {}
        color = random.choice([-1, 1])
        
        self.Userscolor[self.users[0]] = color
        self.colorUsers[color] = self.users[0]

        self.Userscolor[self.users[1]] = self.InverseColor(color)
        self.colorUsers[self.InverseColor(color)] = self.users[1]
