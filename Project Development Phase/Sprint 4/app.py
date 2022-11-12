from urllib import request
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from connection import *
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mail = Mail(app)  # instantiate the mail class
mail.init_app(app)

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ssashokkumar@student.tce.edu'
app.config['MAIL_PASSWORD'] = 'Summa@ITOM'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def index():
    if not session.get("name"):
        return render_template("index.html")
    return redirect("/homepage")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'ml' in request.form and 'p' in request.form:
        ml = request.form['ml']
        pas = request.form['p']

        stmt = "select * from creds where email=? and pass=?"
        prep = ibm_db.prepare(conn, stmt)
        ibm_db.bind_param(prep, 1, ml)
        ibm_db.bind_param(prep, 2, pas)
        res = ibm_db.execute(prep)
        data = ibm_db.fetch_assoc(prep)
        if data:
            session["name"] = data["UNAME"]
            session["email"] = data["EMAIL"]
            return redirect("/homepage")
        else:
            print("Invalid Login")
    return render_template('login.html')


@ app.route("/logout")
def logout():
    session["name"] = None
    return render_template("index.html")


@ app.route("/homepage")
def homepage():
    if not session.get("name"):
        return redirect("/index")
    return render_template('homepage.html')


@ app.route('/eligiblity')
def eligiblity():
    return render_template('eligiblity.html')


@ app.route('/reqform')
def reqform():
    return render_template('reqform.html')


@ app.route('/donordir', methods=['GET', 'POST'])
def donordir():
    l = []
    pdata = []
    if not session.get("name"):
        if request.method == 'POST':
            pname = request.form['name']
            age = request.form['age']
            pbgrp = request.form['bgrp']
            pmno = request.form['mno']
            hname = request.form['hname']
            haddr = request.form['addr']
            pdis = request.form['dis']
            stmt = "SELECT uname,email,blood_group FROM creds WHERE willing='Y' AND  district=?"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, pdis)
            res = ibm_db.execute(prep)
            data = ibm_db.fetch_assoc(prep)
            print("Plus")
            l.append(data)
            pdata.append(pname)
            pdata.append(age)
            pdata.append(pmno)
            pdata.append(hname)
            pdata.append(haddr)
            pdata.append(pdis)
            if (data):
                for item in l:
                    uname = item['UNAME']
                    email = item['EMAIL']
                    dbgrp = item['BLOOD_GROUP']
                    print(uname+" "+dbgrp)
                    if (plasmaMatchCheck(pbgrp, dbgrp)):
                        plasmaRequestMail(email, pdata)
                return render_template('donordir.html', req=len(l))
            else:
                # Display No Donor Avail
                print("D Unavail")
        return render_template('donordir.html', req=0)
    else:
        return render_template('logdonordir.html')


@ app.route('/logdonordir')
def logdonordir():
    stmt = "SELECT uname,age,district,blood_group FROM creds WHERE willing='Y'"
    res = ibm_db.exec_immediate(conn, stmt)
    data = ibm_db.fetch_assoc(res)
    l = []
    l.append(data)
    if not session.get("name"):
        return render_template('donordir.html', data=l)
    return render_template('logdonordir.html', data=l)


@ app.route("/profile", methods=['GET', 'POST'])
def profile():
    if not session.get("name"):
        return redirect("/index")

    stmt = "select * from creds where email=?"
    sql = session["email"]
    prep = ibm_db.prepare(conn, stmt)
    ibm_db.bind_param(prep, 1, sql)
    res = ibm_db.execute(prep)
    data = ibm_db.fetch_assoc(prep)
    print(data)
    if (data):
        phno = data["PHONENO"]
        age = data["AGE"]
        sex = data["SEX"]
        state = data["STATE"]
        dis = data["DISTRICT"]
        bgrp = data["BLOOD_GROUP"]
        will = data["WILLING"]

    if request.method == 'POST':
        phno = request.form['phno']
        age = request.form.get('age')
        sex = request.form.get('sex')
        state = request.form.get('state')
        dis = request.form.get('dis')
        bgrp = request.form.get('bgrp')
        will = request.form.get('will')

        if data["PHONENO"] != phno:
            stmt = "UPDATE CREDS SET PHONENO= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, phno)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

        if data["AGE"] != age:
            print("CHNAGE")
            stmt = "UPDATE CREDS SET AGE= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, age)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

        if data["SEX"] != sex:
            stmt = "UPDATE CREDS SET SEX= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, sex)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

        if data['STATE'] != state:
            stmt = "UPDATE CREDS SET STATE= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, state)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

        if data['DISTRICT'] != dis:
            stmt = "UPDATE CREDS SET DISTRICT= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, dis)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

        if data['BLOOD_GROUP'] != bgrp:
            stmt = "UPDATE CREDS SET BLOOD_GROUP= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, bgrp)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

        if data['WILLING'] != will:
            stmt = "UPDATE CREDS SET WILLING= ? WHERE EMAIL=?;"
            prep = ibm_db.prepare(conn, stmt)
            ibm_db.bind_param(prep, 1, will)
            ibm_db.bind_param(prep, 2, session['email'])
            res = ibm_db.execute(prep)

    return render_template('profile.html', phno=phno, age=age, sex=sex, state=state, dis=dis, bgrp=bgrp, will=will)


@ app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'u' in request.form and 'mail' in request.form and 'phno' in request.form and 'p' in request.form:
        uname = request.form['u']
        ml = request.form['mail']
        pas = request.form['p']
        ph = request.form['phno']

        stmt = "select * from creds where email= ?"
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


def plasmaRequestMail(demail, pdata):
    msg = Message(
        'Important - Plasma Request',
        sender='requestplasma@plasmadonorapp.com',
        recipients=[demail]
    )
    try:
        cont = 'Hello Donor, We are in need of your help to save a Life. \n Patient Name: ' + \
            pdata[0]+"\n Patient Age: "+pdata[1]+"\n Patient Mobile Number: " + \
            pdata[2]+"\n Hospital Name: "+pdata[3]+"\n Hospital Address: "+pdata[4] + \
            "\n\n We kindly request Donors to verify the Paitent data via Mobile Number and Hospital data before proceeding."
        msg.body = cont
        mail.send(msg)
    except:
        print('Unable to send Email')


if __name__ == "__main__":
    app.run(use_reloader=True)
# Auto Reload of Site
# flask --app app.py --debug run
