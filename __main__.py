
from flask import Flask, request, url_for
from flask import redirect
import os

from Game.GameCore import Game
from Users import DB
from Users.JSON import TempJson
from Users.DB import UsersDataBase
from Users.Mails import SendMail
import random, string
from Game.GameCore import Board

app = Flask(__name__)

def GenerateRandomCode(length = random.randint(8, 16)):
    letters = "01234567890" + string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def GetRandomCicat():
    return random.choice(open("static/citata.txt", "r", encoding='utf-8').read().split(';'))

@app.route('/', methods=['POST', 'GET'])
def index():
    ipUser = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if request.method == 'GET':
        if not UsersDataBase.UserDefined(Ip = ipUser): return open("static/html/start.html", "r", encoding="utf-8").read()
        else: return redirect(url_for("StartGame"), code=302)

    elif request.method == 'POST':
        login = request.form["login"]
        TempJson.AddUser(login)
        TempJson.AddProperty(login, "ip", ipUser)
        TempJson.AddProperty(login, "mail", request.form["email"])
        TempJson.AddProperty(login, "password", request.form["password"])
        TempJson.AddProperty(login, "code", GenerateRandomCode())

        return redirect(url_for("Mail"), code=302)
        
@app.route('/mail', methods=['POST', 'GET'])
def Mail():
    ipUser = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    login = TempJson.GetNameByIP(ipUser)
    mailUser = TempJson.GetPropertyUser(login, "mail")
    if request.method == "GET":

        
        SendMail.SendMail(mailUser, TempJson.GetPropertyUser(login, "code"))
        htmlCode = open("static/html/mail.html", "r", encoding="utf-8").read()
        htmlCode = htmlCode.replace("mail_sended", mailUser)
        return htmlCode

    if request.method == "POST":
      code = TempJson.GetPropertyUser(login, "code")
      codeInput = request.form["code"]

      if code != codeInput:
        htmlCode = open("static/html/mail.html", "r", encoding="utf-8").read()
        htmlCode = htmlCode.replace("mail_sended", mailUser)
        htmlCode = htmlCode.replace("hidden", "visible")
        return htmlCode
      else:
        DB.UsersDataBase.AddUser(ipUser, login, TempJson.GetPropertyUser(login, "password"), TempJson.GetPropertyUser(login, "mail"))
        TempJson.DeleteUser(login)
        return redirect(url_for("StartGame"), code=302)

@app.route('/game', methods = ['POST', 'GET'])
def StartGame():
    ipUser = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    login = DB.UsersDataBase.GetNameByIp(ipUser)
    if request.method == "GET":
        return open("static/html/game.html", "r", encoding="utf-8").read().replace("cicata", GetRandomCicat())
    elif request.method == "POST":

        if (request.form["findgame"]  == "Найти партию"):
            users = TempJson.GetAllPossibleUsers(login)
            selfStatus = TempJson.GetStatus(login)
            
            if users == [] and selfStatus == "find":
                TempJson.SetUserGame(login, "find")

                return open('static/html/waiting.html', 'r', encoding='utf-8').read()
            elif users != [] and selfStatus == "find":
                user = random.choice(users)

            else:
                user = TempJson.GetOpponent(login)
            htmlCode = open("static/html/startgame.html", "r", encoding="utf-8").read()

            htmlCode = htmlCode.replace("user", user)
            htmlCode = htmlCode.replace("game", "")
            gamesNow = TempJson.ImportData("Online.json")["Games"].values()
            if not [user, login] in gamesNow and not [login, user] in gamesNow:
                game = Game([user, login])
                TempJson.SetUserGame(login, "inGame")
                TempJson.SetUserGame(user, "inGame")
                TempJson.AddGame(game)
                return redirect(url_for(f"game/{game.code}"), code=302)

            return htmlCode
        return "1"

@app.route('/game/<code>')
def game(code):
    ipUser = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    login = DB.UsersDataBase.GetNameByIp(ipUser)
    game = TempJson.GetGame(code)
    status = TempJson.GetStatus(login)
    board = Board(game["desk"])
    htmlBoard = board.GetBoardString()
    oppent = TempJson.GetOpponent(login)
    htmlCode = open("static/html/startgame.html", "r", encoding="utf-8").read()
    htmlCode = htmlCode.replace("Ураа, вы нашли игру с user!", f"Вы играете против {oppent}")
    htmlCode = htmlCode.replace("game", htmlBoard)
    if request.method == "GET":
        if status == "move":
            htmlCode = htmlCode.replace('hidden', 'visible')
            return htmlCode
        elif status == "waitingMove":
            return htmlCode

    elif request.method == "POST":
        move = request[move]
        fromCell, toCell = move.split(";")

        move = board.Move(list(map(int, fromCell.split())), list(map(int, toCell.split())))
        if move:
            game["desk"] = board.desk
            TempJson.SetUserGame(login, "waitingMove")
            TempJson.SetUserGame(oppent, "move")
            return htmlCode.replace('visible', 'hidden')
        elif not move:
            return htmlCode
        else:
            return "Мат поставлен!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)