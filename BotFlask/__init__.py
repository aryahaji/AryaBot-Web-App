from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI']
app.config['MAIL_SERVER']
app.config['MAIL_PORT']
app.config['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] 
app.config['MAIL_PASSWORD'] 
mail = Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category= 'info'

from BotFlask import routes
