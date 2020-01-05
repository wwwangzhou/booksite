from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # create an instance of Flask class

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qqshruedpiwhwp:8682f7032ddda8eb1e3c53b8845a3c024352367165c2f7f4cc908f427831fb0b@ec2-174-129-33-139.compute-1.amazonaws.com:5432/ddtlmm5cjo2b84'

db = SQLAlchemy(app) # For app initialization

# import os,datetime, csv
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
#
# engine = create_engine(os.getenv("DATABASE_URL"))# bridge the connection between Python and Database
# db = scoped_session(sessionmaker(bind=engine))# allow each user have her/his own workspace
#
# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
#
# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from booksite import routes
