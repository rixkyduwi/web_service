#curl -u john:hello http://127.0.0.1:7002/
import os
from ipaddress import ip_address
from flask import Flask, redirect, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import json
project_dirlogin = os.path.dirname(os.path.abspath(__file__))
database_filelogin = "sqlite:///{}".format(os.path.join(project_dirlogin, "login.db"))
dblogin = SQLAlchemy()
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'rahasia_negara'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    dblogin.init_app(app)

    # blueprint for auth routes in our app
    from .security_authbasic import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
    
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_filelogin
auth = HTTPBasicAuth()
# nama kelompok 
# rizky dwi saputra (6A) 
# muh saefudin fikri (6B) 
class login(dblogin.Model):
    username = dblogin.Column(dblogin.String(80), unique=True, nullable=False, primary_key=True)
    password = dblogin.Column(dblogin.String(100))
    keterangan = dblogin.Column(dblogin.String(100))
users = login.query.all()
pswd=generate_password_hash("123")
print(pswd)

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    

@app.route('/api/v1/login') 
@auth.login_required
def index():
    #return redirect("localhost:4000/api/v2/users/info")
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug = True, port=4000)
