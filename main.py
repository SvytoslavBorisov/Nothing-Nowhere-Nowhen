from flask import Flask, render_template, redirect, request, url_for
from data import db_session, users, questions
from flask_wtf import FlaskForm
from flask_ngrok import run_with_ngrok
import datetime
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.categories import Category

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")


@app.route('/')
def index1():
    return redirect('/main_page')


@app.route('/main_page', methods=['POST', 'GET'])
def main_page():
    session = db_session.create_session()

    param = {}

    param['title'] = 'Главная страница'
    param['style'] = '/static/css/styleForMainPage.css'
    param['script'] = '/static/scripts/scriptFor_main_page.js'
    param['categories'] = session.query(Category).all()

    if request.method == 'GET':
        return render_template('main_page.html', **param)
    elif request.method == 'POST':
        return render_template('main_page.html', **param)


def main():
    db_session.global_init("db/baseDate.sqlite")
    app.run()


main()
