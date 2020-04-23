import os

from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from tempfile import mkdtemp
from flask_mysqldb import MySQL
from flask_session import Session
from app import * 
from passlib.hash import bcrypt
from functools import wraps
import nexmo

# Initialization of methods
app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True, static_url_path="", static_folder="static")
#app.config.from_pyfile('config.cfg')



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'farmer'
app.config['SECRET_KEY'] = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['API_KEY'] = '4933d335'


mysql=MySQL(app)
Session(app)

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("n_id") is None:
            return redirect(url_for("main.index", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def enterprise_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("e_id") is None:
            return redirect(url_for("main.index", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect(url_for("main.index", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#Importing Blueprints
from app.views.main import main
#from app.views.admin import admin
#from app.views.admin import enterprise

#Registering Blueprints
app.register_blueprint(main)
#app.register_blueprint(admin)
#app.register_blueprint(enterprise)

