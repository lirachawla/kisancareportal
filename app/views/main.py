import os

from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from tempfile import mkdtemp
from flask_mysqldb import MySQL
from flask_session import Session
from app import *
from passlib.hash import bcrypt
from datetime import date
from twilio.rest import Client
from credentials import account_sid,auth_token,my_cell,my_twilio

main = Blueprint('main', __name__)

eid=""
def execute_db(query,args=()):
    try:
        cur=mysql.connection.cursor()
        cur.execute(query,args)
        mysql.connection.commit()
    except:
        mysql.connection.rollback()
    finally:
        cur.close()

def query_db(query,args=(),one=False):
    cur=mysql.connection.cursor()
    result=cur.execute(query,args)
    if result>0:
        values=cur.fetchall()
        return values
    cur.close()


@main.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", **locals())

@main.route("/statistics/", methods=["POST", "GET"])
def faq():
    return render_template("stats.html")

@main.route("/farmer_signup/", methods=["POST", "GET"])
def farmer_signup():
    if request.method=="POST":

        fname=request.form["fname"]
        mname=request.form["mname"]
        lname=request.form["lname"]
        district=request.form["district"]
        area=request.form["area"]
        mobile=request.form["fphone"]
        aadhar=request.form["faadhaar"]
        account=request.form["faccount"]


        execute_db("INSERT INTO farmer(fname, mname, lname , mobile, district, area, aadhar, account) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (fname, mname, lname, district, area, mobile, aadhar, account, ))
        execute_db("INSERT INTO crops(fmobile, district) VALUES (%s, %s);", (mobile, district,))
        return redirect(url_for('main.farmer_login'))

    return render_template("farmer_signup.html")

@main.route("/enterprise_signup/", methods=["POST", "GET"])
def enterprise_signup():
    if request.method=="POST":

        name=request.form["cname"]
        email=request.form["cmail"]
        mobile=request.form["cphone"]
        investment=request.form["inv"]
        gstin=request.form["cgst"]
        password=request.form["cpass"]


        execute_db("INSERT INTO enterprise(name, email, mobile, investment, gstin, password) VALUES (%s, %s, %s, %s, %s, %s);", (name, email, mobile, investment, gstin, password, ))
        return redirect(url_for('main.enterprise_login'))

    return render_template("enterprise_signup.html")

@main.route("/farmer_login/", methods=["POST", "GET"])
def farmer_login():
    if request.method=="POST":
        username = request.form["id"]
        password = request.form["pass"]
        #query  = query_db("SELECT password FROM farmer WHERE n_id=%s;",(username, ))
        #if query is None:
        #    flash("Incorrect Credentials!", "danger")
        #    return redirect(url_for('main.login'))
        #else:
            # print(query)
        if password==username:
            session["n_id"] = username
            flash("Login Successful", "success")
            return redirect(url_for('main.farmer'))
    
        else:
            flash("Incorrect Credentials", "danger")
            return redirect(url_for('main.index'))
    return render_template("farmer_login.html", **locals())

@main.route("/admin_login/", methods=["POST", "GET"])
def admin_login():
    if request.method=="POST":
        username = request.form["id"]
        password = request.form["pass"]
        #query  = query_db("SELECT password FROM farmer WHERE n_id=%s;",(username, ))
        #if query is None:
        #    flash("Incorrect Credentials!", "danger")
        #    return redirect(url_for('main.login'))
        #else:
            # print(query)
        if password==username:
            session["admin_id"] = username
            id=username
            flash("Login Successful", "success")
            return redirect(url_for('main.admin'))
    
        else:
            flash("Incorrect Credentials", "danger")
            return redirect(url_for('main.index'))
    return render_template("admin_login.html", **locals())

@main.route("/enterprise_login/", methods=["POST", "GET"])
def enterprise_login():
    if request.method=="POST":
        username = request.form["id"]
        password = request.form["pass"]
        #query  = query_db("SELECT password FROM farmer WHERE n_id=%s;",(username, ))
        #if query is None:
        #    flash("Incorrect Credentials!", "danger")
        #    return redirect(url_for('main.login'))
        #else:
            # print(query)
        if password==username:
            session["e_id"] = username
            flash("Login Successful", "success")
            return redirect(url_for('main.enterprise'))
    
        else:
            flash("Incorrect Credentials", "danger")
            return redirect(url_for('main.index'))
    return render_template("enterprise_login.html", **locals())


@main.route('/logout/', methods=["GET", "POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("main.index"))

@main.route('/farmer/', methods=["GET", "POST"])
@login_required
def farmer():

    fun=0
    
    queries = query_db("SELECT * FROM crops WHERE crop is not NULL;")
    if queries is None:
        queries = []
    for query in queries:
        if query[1]=="1":
            fun=1
        elif query[1]=="2":
            fun=2
        elif query[1]=="3":
            fun=3
        elif query[1]=="4":
            fun=4

    
    return render_template("farmer.html", fun=fun)

@main.route('/admin/', methods=["GET", "POST"])
@admin_required
def admin(): 
    if request.method=="POST":
        # Load in configuration from environment variables:
        NEXMO_API_KEY = '4933d335'
        NEXMO_API_SECRET = 'NOKce7yUQ0xUlbsi'
        NEXMO_NUMBER = 6283412390

        number = request.form['destination']
        message = request.form['message']
 
        # Create a new Nexmo Client object:
        client = nexmo.Client(
            key=NEXMO_API_KEY, secret=NEXMO_API_SECRET
        )

        response=client.send_message({'from' : '6283412390', 'to' : number, 'text' : message})

    ric=0
    whe=0
    mai=0
    oth=0
    bhoj=0
    patn=0
    muzz=0
    madh=0
    s1=0
    m1=0
    h1=0
    s=0
    m=0
    h=0
    t=0
    n=0

    queries = query_db("SELECT * FROM crops;")
    if queries is None:
        queries = []
    for query in queries:
        if query[6]=="1":
            bhoj=bhoj+1
        elif query[6]=="3":
            patn=patn+1
        elif query[6]=="4":
            muzz=muzz+1
        elif query[6]=="2":
            madh=madh+1

        if query[1]=="1":
            ric=ric+1
        elif query[1]=="2":
            whe=whe+1
        elif query[1]=="3":
            mai=mai+1
        elif query[1]=="4":
            oth=oth+1

        if query[2]!="":
            s1=s1+1
            t=t+1
        if query[3]!="":
            m1=m1+1
            t=t+1
        if query[4]!="":
            h1=h1+1
            t=t+1

        if query[5]=="y":
            n=n+1

        s=s1*100/t
        m=m1*100/t
        h=h1*100/t




    return render_template("admin.html", ric=ric, whe=whe, mai=mai, oth=oth, bhoj=bhoj, patn=patn, muzz=muzz, madh=madh, s=s, m=m, h=h, n=n)

@main.route('/enterprise/', methods=["GET", "POST"])
@enterprise_required
def enterprise():
    return render_template("enterprise.html", **locals())

@main.route('/logout_admin/', methods=["GET", "POST"])
@admin_required
def logout_admin():
    session.clear()
    return redirect(url_for("main.index"))

@main.route('/logout_enterprise/', methods=["GET", "POST"])
@enterprise_required
def logout_enterprise():
    session.clear()
    return redirect(url_for("main.index"))


@main.route('/add_yojna/', methods=["GET", "POST"])
@enterprise_required
def add_yojna():

    if request.method=="POST":

        name=request.form["name"]
        description=request.form["description"]
        budget=request.form["budget"]

        execute_db("INSERT INTO yojna(gstin, name, description, budget) VALUES (%s, %s, %s, %s);", (eid, name, description, budget, ))
    return redirect(url_for("main.enterprise"))

crop1="1"
no="1234567890"

@main.route('/add_rice/', methods=["GET", "POST"])
@login_required
def add_rice():

    if request.method=="POST":
        execute_db("UPDATE crops SET crop = %s WHERE fmobile = %s;", (crop1, no,))

    return redirect(url_for("main.farmer"))

crop2="2"

@main.route('/add_wheat/', methods=["GET", "POST"])
@login_required
def add_wheat():

    if request.method=="POST":
        execute_db("UPDATE crops SET crop = %s WHERE fmobile = %s;", (crop2, no, ))

    return redirect(url_for("main.farmer"))

crop3="3"

@main.route('/add_maize/', methods=["GET", "POST"])
@login_required
def add_maize():

    if request.method=="POST":
        execute_db("UPDATE crops SET crop = %s WHERE fmobile = %s;", (crop3, no, ))

    return redirect(url_for("main.farmer"))

crop4="4"

@main.route('/add_others/', methods=["GET", "POST"])
@login_required
def add_others():

    if request.method=="POST":
        execute_db("UPDATE crops SET crop = %s WHERE fmobile = %s;", (crop4, no, ))

    return redirect(url_for("main.farmer"))

@main.route('/sowdate/', methods=["GET", "POST"])
@login_required
def sowdate():

    if request.method=="POST":
        date=request.form["sdate"]
        execute_db("UPDATE crops SET sowdate = %s WHERE fmobile = %s;", (date, no,))

    return redirect(url_for("main.farmer"))

@main.route('/mandate/', methods=["GET", "POST"])
@login_required
def mandate():

    if request.method=="POST":
        date=request.form["mdate"]
        execute_db("UPDATE crops SET mandate = %s WHERE fmobile = %s;", (date, no,))

    return redirect(url_for("main.farmer"))

@main.route('/hardate/', methods=["GET", "POST"])
@login_required
def hardate():

    if request.method=="POST":
        date=request.form["hdate"]
        execute_db("UPDATE crops SET hardate = %s WHERE fmobile = %s;", (date, no,))

    return redirect(url_for("main.farmer"))


@main.route('/login_portal/', methods=["GET", "POST"])
def login_portal():
    return render_template("login_portal.html", **locals())

@main.route('/send_msg/', methods=["GET", "POST"])
@admin_required
def send_msg():

    if request.method=="POST":
        mymsg = request.form['message']
        client =Client(account_sid, auth_token)

        message=client.messages.create(to=my_cell,from_=my_twilio,body=mymsg)
    return redirect(url_for("main.admin"))

@main.route('/add_ann/', methods=["GET", "POST"])
@admin_required
def add_ann():

    if request.method=="POST":
        
        return redirect(url_for("main.admin"))