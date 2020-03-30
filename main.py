from flask import Flask, render_template, redirect, request, url_for
from data import db_session, users, questions
from flask_wtf import FlaskForm
from flask_ngrok import run_with_ngrok
import datetime
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index1():
    return redirect('/main_page')


@app.route('/main_page', methods=['POST', 'GET'])
def main_page():
    param = {}

    param['title'] = 'Главная страница'
    param['style'] = '/static/css/styleForMainPage.css'
    param['script'] = '/static/scripts/scriptFor_main_page.js'

    if request.method == 'GET':
        return render_template('main_page.html', **param)
    elif request.method == 'POST':
        return render_template('main_page.html', **param)


def main():
    db_session.global_init("db/baseDate.sqlite")

main()
