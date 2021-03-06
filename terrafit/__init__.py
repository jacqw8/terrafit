from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eFTnnv5mZnAU-eMa0C2uyA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
cwd = os.getcwd()
app.config['UPLOAD_PATH'] = cwd + '/terrafit/clothes'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from terrafit import routes
