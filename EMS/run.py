from routes import app
from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user

if __name__ == '__main__':

    app.run(debug=True)


