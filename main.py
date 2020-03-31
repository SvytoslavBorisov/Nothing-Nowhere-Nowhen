from flask import Flask, render_template, redirect, request, url_for
from data import db_session, users, questions
from flask_wtf import FlaskForm
from flask_ngrok import run_with_ngrok
import datetime
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.categories import Category
from data.questions import Question
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_question import AddQuestionForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")


@app.route('/')
def index1():
    logout_user()
    return redirect('/categories')


@app.route('/categories', methods=['POST', 'GET'])
def main_page():
    session = db_session.create_session()

    param = {}

    param['title'] = 'Главная страница'
    param['style'] = '/static/css/styleForMainPage.css'
    param['script'] = ''
    param['categories'] = session.query(Category).all()

    if request.method == 'GET':
        return render_template('categories.html', **param)
    elif request.method == 'POST':
        return render_template('categories.html', **param)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session = db_session.create_session()
    param = {}

    param['title'] = 'Главная страница'
    param['style'] = '/static/css/styleForLogin.css'
    param['script'] = ''

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/categories')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **param)
    return render_template('login.html', form=form, **param)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['POST', 'GET'])
def register():
    session = db_session.create_session()
    param = {}

    param['title'] = 'Главная страница'
    param['style'] = '/static/css/styleForRegister.css'

    form = RegisterForm()
    if form.validate_on_submit():
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user:
            return render_template('register.html',
                                   message="Пользователь с такой почтой уже есть",
                                   form=form, **param)
        else:
            user = session.query(users.User).filter(users.User.nickname == form.nickname.data).first()
            if user:
                return render_template('register.html',
                                       message="Пользователь с таким ником уже есть",
                                       form=form, **param)
            else:
                user = users.User()
                user.name = request.form['name']
                user.surname = request.form['surname']
                user.nickname = request.form['nickname']

                user.email = request.form['email']
                user.set_password(request.form['password'])
                session.add(user)
                if request.files.get('file'):
                    f = request.files['file']
                    user.avatar = f'static/img/users_avatars/{user.id}.png'
                    with open(user.avatar, 'wb') as f1:
                        f1.write(f.read())
                session.commit()
                login_user(user)

                return redirect('/categories')

    return render_template('register.html', form=form, **param)


@app.route('/user_info/<string:user>')
@login_required
def user_info(user):
    param = {}

    param['title'] = 'Профиль'
    param['style'] = '/static/css/styleForUserInfo.css'

    return render_template('user_info.html', **param)


@app.route('/add_question/<string:user>', methods=['POST', 'GET'])
@login_required
def add_question(user):
    session = db_session.create_session()
    param = {}

    param['title'] = 'Создать вопрос'
    param['style'] = '/static/css/styleForAddQuestion.css'

    form = AddQuestionForm()
    if form.validate_on_submit():
        question = Question()
        question.text = request.form['text']
        question.category = session.query(Category).filter(Category.name == request.form['category']).first().id
        question.answers = "!@#$%".join([request.form['answer'], request.form['wrong_answer1'], request.form['wrong_answer2'], request.form['wrong_answer3']])
        question.right_answer = request.form['answer']
        question.who_add = current_user.id
        if current_user.state == "admin":
            question.is_promoted = True
        else:
            question.is_promoted = False
        session.add(question)
        session.commit()

        return redirect(f'/user_info/{user}')

    return render_template('add_question.html', form=form, **param)


app.run()
