from flask import Flask, request, redirect, url_for, session
from datetime import timedelta
from json import dumps

class Messages():

    def __init__(self):

        self.not_logged_in_default = {"error": True, "message":"you are not logged in. please login by sending POST request to /login"}
        self.not_logged_in_attempted_logout = {"error": True, "message":"you have tried to logout without logging in first"}
        self.not_logged_in_invalid_credentials = {"error": True, "message": "your credentials were invalid"}
        self.logged_in = {"error": False, "message":"you are now logged in","username":""}
        self.logged_out = {"error": False, "message":"you are now logged out"}
        self.all_ok = {"error":False, "message":"everything went fine"}
        self.throw_a_dice_success = {"was_throw_succesfull":True, "message":"you win"}
        self.throw_a_dice_fail = {"was_throw_succesfull":False, "message":"you lose"}
        self.invalid_method = {}

app = Flask(__name__)

app.secret_key = "niggerman"


@app.route("/")
def home():
    m = Messages()
    if "loggedin" in session:
        if session["loggedin"] != True:
            jd = dumps(m.not_logged_in_default)
    else:
        cd = m.logged_in
        cd.update("username",session["username"])
        jd = dumps(cd)
    return jd

@app.route("/login", methods=["POST","GET"])
def login():
    m = Messages()
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        if user == "juzek" and password == "chui":
            session['loggedin'] = True
            session['username'] = user
            jd = dumps(m.logged_in.format(user))
        else:
            session['loggedin'] = False
            jd = dumps(m.not_logged_in_invalid_credentials)
        return jd
    else:
        jd = dumps(m.invalid_method)
        return jd


@app.route("/profile")
def profile():
    m = Messages()
    if session["loggedin"] != True:
        jd = dumps(m.not_logged_in_default)
    else:
        jd = dumps(m.logged_in.format(session["loggedin"]))
    return jd

@app.route("/logout")
def logout():
    m = Messages()
    if "loggedin" in session:
        if session["loggedin"] == True:
            session.pop("username",None)
            session.pop("loggedin",None)
            jd = dumps(m.logged_out)
        else:
            jd = dumps(m.not_logged_in_attempted_logout)
    else:
        jd = dumps(m.not_logged_in_attempted_logout)
    return jd

@app.route("/play")
def play():
    return "tu bedzierz rzucal kostka"

if __name__ == "__main__":
    app.run()
