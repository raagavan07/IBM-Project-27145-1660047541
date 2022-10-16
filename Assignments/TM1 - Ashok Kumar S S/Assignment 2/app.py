from urllib import request
from flask import Flask, render_template, redirect, request
from connection import *
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def reg():
    tuple = True
    if request.method == 'POST':
        ml = request.form['mail']
        un = request.form['uname']
        pas = request.form['pass']

        stmt = "select * from Ass where email= ?"
        prep = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep, 1, ml)
        res = ibm_db.execute(prep)
        tuple = ibm_db.fetch_row(prep)

        if (tuple == False):
            stmt = "insert into Ass values(?,?,?);"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, un)
            ibm_db.bind_param(prep, 2, ml)
            ibm_db.bind_param(prep, 3, pas)
            res = ibm_db.execute(prep)
            print("Account Created Successfully")
            return redirect("/login")
        else:
            print("Account Already Exist")
    return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'mail' in request.form and 'pass' in request.form:
        ml = request.form['mail']
        pas = request.form['pass']

        stmt = "select * from Ass where email=? and pass=?"
        prep = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep, 1, ml)
        ibm_db.bind_param(prep, 2, pas)
        res = ibm_db.execute(prep)
        data = ibm_db.fetch_assoc(prep)
        if data:
            return redirect("/welcome")
        else:
            return redirect("/")
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    app.run(debug=True)
