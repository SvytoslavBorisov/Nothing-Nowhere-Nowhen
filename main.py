from flask import Flask, render_template, redirect, request, url_for
from data import db_session, users, questions
from datetime import datetime
from flask_wtf import FlaskForm
from flask_ngrok import run_with_ngrok
import datetime
import socket
import struct
import time
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.categories import Category
from data.questions import Question
from data.users import User
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_question import AddQuestionForm
from random import choice, shuffle

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")


def get_time():
    address = ('pool.ntp.org', 123)
    msg = '\x1b' + '\0' * 47

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(bytes(msg, encoding='utf-8'), address)
    msg, _ = client.recvfrom(1024)

    secs = struct.unpack("!12I", msg)[10] - 2208988800
    return secs


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
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session = db_session.create_session()
    param = {}

    param['title'] = 'Главная страница'
    param['style'] = '/static/css/styleForLogin.css'
    param['script'] = ''

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
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
        user = session.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template('register.html',
                                   message="Пользователь с такой почтой уже есть",
                                   form=form, **param)
        else:
            user = session.query(User).filter(User.nickname == form.nickname.data).first()
            if user:
                return render_template('register.html',
                                       message="Пользователь с таким ником уже есть",
                                       form=form, **param)
            else:
                user = User()
                user.name = request.form['name']
                user.surname = request.form['surname']
                user.nickname = request.form['nickname']
                user.email = request.form['email']
                user.set_password(request.form['password'])
                user.rating = 0
                user.wins = 0
                user.defeats = 0
                user.add_questions = 0
                user.games = 0
                session.add(user)
                session.commit()
                if request.files.get('file'):
                    f = request.files['file']
                    user.avatar = f'static/img/users_avatars/{user.id}.png'
                    with open(user.avatar, 'wb') as f1:
                        f1.write(f.read())
                else:
                    user.avatar = f'static/img/users_avatars/no_photo.png'
                session.commit()
                login_user(user)

                return redirect('/categories')

    return render_template('register.html', form=form, **param)


@app.route('/user_info/<string:user>')
def user_info(user):
    session = db_session.create_session()
    param = {}

    param['title'] = 'Профиль'
    param['style'] = '/static/css/styleForUserInfo.css'
    param['user'] = session.query(User).filter(User.nickname == user).first()
    if param['user'].games:
        param['procent_win'] = int((param['user'].wins / param['user'].games) * 100)
        param['procent_def'] = int(100 - param['procent_win'])
    else:
        param['procent_win'] = 100
        param['procent_def'] = 100

    return render_template('user_info.html', **param)


@app.route('/add_question/<string:user>', methods=['POST', 'GET'])
@login_required
def add_question(user):
    session = db_session.create_session()
    param = {}

    param['title'] = 'Создать вопрос'
    param['style'] = '/static/css/styleForAddQuestion.css'
    param['categories'] = session.query(Category).all()

    form = AddQuestionForm()
    form.category.choices = [(x.name, x.name) for x in param['categories']]
    form.category.default = param['categories'][0].name
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


@app.route('/about_site', methods=['POST', 'GET'])
def about_site():
    param = {}

    param['title'] = 'О сайте'
    param['style'] = '/static/css/styleForAboutSite.css'
    return render_template('about_site.html', **param)


@app.route('/game/<int:id_>')
def game(id_):
    session = db_session.create_session()
    param = {}

    param['title'] = 'Начать игру'
    param['style'] = '/static/css/styleForGame.css'
    param['category'] = session.query(Category).filter(Category.id == id_).first()

    return render_template('game.html', **param)


@app.route('/start_game/<int:id_>')
def start_game(id_):
    session = db_session.create_session()

    quests = []
    for question in session.query(Question).filter(Question.category == id_):
        quests.append(question)
    selected = []
    for _ in range(min(len(quests), 6)):
        k = choice(quests)
        while k in selected:
            k = choice(quests)
        selected.append(k)
    temp_data = ['0', '1', '2', '3']
    shuffle(temp_data)
    return redirect(f'/current_game/{"!@$".join([str(x.id) for x in selected]) + "!@$" +  "".join(temp_data) + "!@$" + "0" + "!@$" + str(get_time())}')


@app.route('/current_game/<quests>', methods=['POST', 'GET'])
def current_game(quests):
    session = db_session.create_session()
    param = {}
    questions = quests.split('!@$')
    param['current_time'] = get_time() - int(questions[-1])

    param['title'] = 'Идёт игра'
    param['style'] = '/static/css/styleForCurrentGame.css'
    param['question'] = session.query(Question).filter(Question.id == int(questions[int(questions[-2])])).first()
    param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()
    param['answers'] = ['', '', '', '']
    param['answers'][0] = param['question'].answers.split('!@#$%')[int(questions[-3][0])]
    param['answers'][1] = param['question'].answers.split('!@#$%')[int(questions[-3][1])]
    param['answers'][2] = param['question'].answers.split('!@#$%')[int(questions[-3][2])]
    param['answers'][3] = param['question'].answers.split('!@#$%')[int(questions[-3][3])]
    param['current_number_quest'] = int(questions[-2])
    temp = quests.split('!@$')[:-3]
    param['path'] = f'/next_quest/{"!@$".join([x for x in temp]) + "!@$" + questions[-3] + "!@$" + str(param["current_number_quest"]) + "!@$" + "time"}'
    if request.method == 'GET':
        if param['current_time'] > 60:
            result = False
            return redirect(f'/next_quest/{"!@$".join([x for x in temp]) + "!@$" + questions[-3] + "!@$" + str(param["current_number_quest"]) + "!@$" + str(result)}')
        return render_template('current_game.html', **param)
    elif request.method == 'POST':
        if request.form.get('option'):
            if request.form['option'] == param['question'].right_answer:
                result = True
            else:
                result = False
        else:
            result = False
        return redirect(f'/next_quest/{"!@$".join([x for x in temp]) + "!@$" + questions[-3] + "!@$" + str(param["current_number_quest"]) + "!@$" + str(result)}')


@app.route('/next_quest/<quests>', methods=['POST', 'GET'])
def next_quest(quests):
    session = db_session.create_session()
    param = {}
    questions = quests.split('!@$')

    param['result'] = 'Вы ответиили правильно' if questions[-1] == 'True' else 'Вы не успели ответить' if questions[-1] == 'time' else 'Вы неправильно ответили'

    param['title'] = 'Ответ'
    param['style'] = '/static/css/styleForCurrentGame.css'
    param['question'] = session.query(Question).filter(Question.id == int(questions[int(questions[-2])])).first()
    param['answers'] = ['', '', '', '']
    param['answers'][0] = param['question'].answers.split('!@#$%')[int(questions[-3][0])]
    param['answers'][1] = param['question'].answers.split('!@#$%')[int(questions[-3][1])]
    param['answers'][2] = param['question'].answers.split('!@#$%')[int(questions[-3][2])]
    param['answers'][3] = param['question'].answers.split('!@#$%')[int(questions[-3][3])]
    param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()
    param['current_number_quest'] = int(questions[-2])
    temp = quests.split('!@$')[:-3]
    if request.method == 'GET':
        return render_template('next_game.html', **param)
    elif request.method == 'POST':
        temp_data = ['0', '1', '2', '3']
        shuffle(temp_data)
        if param["current_number_quest"] + 1 < len(temp):
            return redirect(f'/current_game/{"!@$".join([x for x in temp]) + "!@$" + "".join(temp_data) + "!@$" + str(param["current_number_quest"] + 1) + "!@$" + str(get_time())}')
        else:
            return redirect('/categories')


@app.route('/rating')
def rating():
    session = db_session.create_session()
    param = {}

    param['title'] = 'Рейтинг'
    param['style'] = 'static/css/styleForRating.css'
    all_users = session.query(User).all()
    all_users.sort(key=lambda x: (-x.rating, x.surname.lower() + x.name.lower(), x.nickname.lower()))
    param['users'] = all_users

    return render_template('rating.html', **param)