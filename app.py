from urllib import request
from flask import Flask, render_template, request
from connection import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    lStatus = ''
    if request.method == 'POST' and 'u' in request.form and 'p' in request.form:
        uname = request.form['u']
        pas = request.form['p']

        if uname == 'admin' and pas == 'admin':
            # session['loggedin'] = True
            # session['username'] = account['username']
            lStatus = 'Welcome Admin'
            return render_template('login.html', lStatus=lStatus)
    return render_template('login.html')


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
