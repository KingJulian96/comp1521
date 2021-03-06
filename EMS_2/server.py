from flask import Flask
from flask_login import LoginManager
from src.ems import EMS

app = Flask(__name__, static_url_path='')
app.secret_key = "what's the meaning of this"
ems = EMS()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def login_user(user_email):
    return ems.check_email(user_email)

