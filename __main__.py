
from flask import Flask, request, url_for
from flask import redirect
import os

from Game.GameCore import Game, GenerateCode
from Users import DB
from Users.JSON import TempJson
from Users.DB import UsersDataBase
from Users.Mails import SendMail
import random, string

app = Flask(__name__)

def GenerateRandomCode(length = random.randint(8, 16)):
    letters = "01234567890" + string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
    
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
    login = TempJson.GetNameByIP(ipUser)
    if request.method == "GET":
        return open("static/html/game.html", "r", encoding="utf-8").read()
    elif request.method == "POST":
        if (request.form["findgame"]  == "Найти партию"):
            TempJson.SetUserGame(login, "find")
            users = TempJson.GetAllPossibleUsers(login)
            if not users: return open('static/html/waiting.html', 'r', encoding='utf-8').read()
            user = random.choice(users)
            htmlCode = open("static/html/startgame.html", "r", encoding="utf-8").read()
            htmlCode = htmlCode.replace("user", user)
            TempJson.SetUserGame(login, "found")
            TempJson.SetUserGame(user, "found")

            
            gamesNow = TempJson.ImportData("Online.json")["Games"].keys()
            if not (GenerateCode([user, login]) in gamesNow and GenerateCode([login, user])):
                game = Game([user, login])
                TempJson.AddGame(game)
    
            return htmlCode
        return "1"
       

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)