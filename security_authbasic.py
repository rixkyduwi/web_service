#curl -u john:hello http://127.0.0.1:7002/
import os
from ipaddress import ip_address
from flask import Flask, redirect, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import json
from flask_login import LoginManager
login_manager = LoginManager()

project_dirlogin = os.path.dirname(os.path.abspath(__file__))
database_filelogin = "sqlite:///{}".format(os.path.join(project_dirlogin, "login.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_filelogin
dblogin = SQLAlchemy(app)
login_manager.init_app(app)
auth = HTTPBasicAuth()
# nama kelompok 
# rizky dwi saputra (6A) 
# moh saefudin fikri (6B) 
class login(dblogin.Model):
    username = dblogin.Column(dblogin.String(80), unique=True, nullable=False, primary_key=True)
    password = dblogin.Column(dblogin.String(100))
    keterangan = dblogin.Column(dblogin.String(100))
users = login.query.all()
print(users)
pswd=generate_password_hash("123")
print(pswd)
@auth.verify_password
def verify_password(username, password):
    username=login.query.filter_by(username=username).first()
    if not username or not check_password_hash(username.password, password):
        return username.keterangan
    

@app.route('/api/v1/login') 
@auth.login_required
def index():
    #return redirect("localhost:4000/api/v2/users/info")
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug = True, port=4000)
