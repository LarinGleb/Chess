
from .Chess import Board
import random

def GenerateCode(Users):
    user_one, user_two = Users
    return str(id(user_one)) + str(id(user_two))

class Game():
    def __init__(self, users, board = Board.Board(), randomColor = True, colors = [], code = ""):
        self.code = code if code != "" else GenerateCode(users)
        self.Board = board
        self.users = users
        if randomColor:
            self.SetColors()
        else:
            self.Userscolor = {}
            self.colorUsers = {}

            self.Userscolor[users[0]] = colors[0]
            self.Userscolor[users[1]] = colors[1]

            self.colorUsers[colors[0]] = users[0]
            self.colorUsers[colors[1]] = users[1]

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
