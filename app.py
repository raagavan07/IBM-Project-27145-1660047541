from urllib import request
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from connection import *

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/")
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST' and 'ml' in request.form and 'p' in request.form:
        ml = request.form['ml']
        pas = request.form['p']

        stmt = "select uname, email, pass from creds"
        res = ibm_db.exec_immediate(conn, stmt)
        dictionary = ibm_db.fetch_both(res)
        while dictionary != False:
            if (dictionary[1] == ml and dictionary[2] == pas):
                session["name"] = dictionary[0]
                print("Valid Login ")
                print(dictionary[0])
                return render_template('homepage.html')
            dictionary = ibm_db.fetch_both(res)
        else:
            print("Invalid Login")
    return render_template('login.html')


@app.route("/logout")
def logout():
    session["name"] = None
    return render_template("index.html")


@app.route("/homepage")
def homepage():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/index")
    return render_template('homepage.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'u' in request.form and 'mail' in request.form and 'phno' in request.form and 'p' in request.form:
        uname = request.form['u']
        ml = request.form['mail']
        pas = request.form['p']
        ph = request.form['phno']

        stmt = "select * from creds where email= ? and pass= ?;"
        prep = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep, 1, ml)
        ibm_db.bind_param(prep, 2, pas)
        res = ibm_db.execute(prep)
        tuple = ibm_db.fetch_row(prep)

        if (tuple == False):
            stmt = "insert into creds values(default,?,?,?,?);"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, uname)
            ibm_db.bind_param(prep, 2, ml)
            ibm_db.bind_param(prep, 3, ph)
            ibm_db.bind_param(prep, 4, pas)
            res = ibm_db.execute(prep)
            print("Account Created Successfully")
        else:
            print("Account Already Exist")
    return render_template('register.html')


if __name__ == "__main__":
    app.run(use_reloader=True)

# Auto Reload of Site
# flask --app app.py --debug run
