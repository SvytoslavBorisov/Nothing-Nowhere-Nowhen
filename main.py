from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session, users, questions
from datetime import datetime
from flask_wtf import FlaskForm
from flask_ngrok import run_with_ngrok
import datetime
import socket
import struct
import time
import random
import json
import os
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.categories import Category
from data.questions import Question
from data.users import User
from data.games import Game
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_question import AddQuestionForm
from random import choice, shuffle
from cryptography.fernet import Fernet
from api import questions_resources, users_resources


app = Flask(__name__)
app.config.update(
    JSON_AS_ASCII=False
)
api = Api(app)
#  app.register_blueprint(questions_api.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")

api.add_resource(questions_resources.QuestionsListResource, '/api/questions')
api.add_resource(questions_resources.QuestionResource, '/api/question/<question_id>')

api.add_resource(users_resources.UsersListResource, '/api/users')
api.add_resource(users_resources.UserResource, '/api/user/<user_id>')


def open_json(file):
    with open(file, "r") as f:
        return json.load(f)


def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def return_to_game():
    data = open_json('static/json/games.json')
    if current_user.is_authenticated and str(current_user.id) in data['current_games'] and data['current_games'][str(current_user.id)] is not None:
        print("yes")
        return 1
    return 0


def get_time():
    address = ('pool.ntp.org', 123)
    msg = '\x1b' + '\0' * 47

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(bytes(msg, encoding='utf-8'), address)
    msg, _ = client.recvfrom(1024)

    secs = struct.unpack("!12I", msg)[10] - 2208988800
    return secs


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/categories')
def categories():
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()

    param = {}

    param['title'] = 'Играть'
    param['style'] = '/static/css/styleForCategories.css'
    param['style_mobile'] = '/static/css_mobile/styleForCategoriesMobile.css'
    param['script'] = ''
    param['categories'] = session.query(Category).all()
    param['img'] = [int(x.split('.')[0]) for x in os.listdir('static/img/categories')]

    if request.method == 'GET':
        return render_template('categories.html', **param)
    elif request.method == 'POST':
        return render_template('categories.html', **param)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    k = return_to_game()
    if k:
        return redirect('/current_game')
    param = {}

    param['title'] = 'Главная страница'
    param['style'] = 'static/css/styleForMainPage.css'
    param['style_mobile'] = '/static/css_mobile/styleForMainPageMobile.css'
    return render_template('main_page.html', **param)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Вход'
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
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Регистрация'
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
                user.all_games = 0
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
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Профиль'
    param['style'] = '/static/css/styleForUserInfo.css'
    param['user'] = session.query(User).filter(User.nickname == user).first()
    param['games'] = param['user'].games
    if param['user'].all_games:
        param['procent_win'] = int((param['user'].wins / param['user'].all_games) * 100)
        param['procent_def'] = int(100 - param['procent_win'])
    else:
        param['procent_win'] = 100
        param['procent_def'] = 100

    return render_template('user_info.html', **param)


@app.route('/add_question/<string:user>', methods=['POST', 'GET'])
@login_required
def add_question(user):
    k = return_to_game()
    if k:
        return redirect('/current_game')
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
        question.comment = request.form['comment']
        session.add(question)
        session.commit()

        return redirect(f'/user_info/{user}')

    return render_template('add_question.html', form=form, **param)


@app.route('/about_site', methods=['POST', 'GET'])
def about_site():
    k = return_to_game()
    if k:
        return redirect('/current_game')
    param = {}

    param['title'] = 'О сайте'
    param['style'] = '/static/css/styleForAboutSite.css'
    param['style_mobile'] = '/static/css_mobile/styleForAboutSiteMobile.css'
    return render_template('about_site.html', **param)


@app.route('/game/<int:id_>')
def game(id_):
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Начать игру'
    param['style'] = '/static/css/styleForGame.css'
    param['category'] = session.query(Category).filter(Category.id == id_).first()

    return render_template('game.html', **param)


@app.route('/start_game/<int:id_>')
def start_game(id_):
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()

    quests = []
    if current_user.is_authenticated:
        for question in session.query(Question).filter(Question.category == id_, Question.who_add != current_user.id):
            quests.append(question)
    else:
        for question in session.query(Question).filter(Question.category == id_):
            quests.append(question)

    selected = []
    for _ in range(min(len(quests), 11)):
        k = choice(quests)
        while k in selected:
            k = choice(quests)
        selected.append(k)

    data = open_json('static/json/games.json')
    if current_user.is_authenticated:
        load = {
            'questions': [x.id for x in selected],
            'wins': 0,
            'defeats': 0,
            'current_question': 0,
            'time': get_time(),
            'quest_or_next': 'quest',
            'last_result': None
        }
        data['current_games'][str(current_user.id)] = {}
        for x in load:
            data['current_games'][str(current_user.id)][x] = load[x]
        print(0)
        print(data)
        save_json(data, 'static/json/games.json')

    return redirect('/current_game')


@app.route('/current_game', methods=['POST', 'GET'])
def current_game():
    session = db_session.create_session()
    if current_user.is_authenticated:
        data = open_json('static/json/games.json')

        print(data['current_games'][str(current_user.id)]['quest_or_next'])

        param = {}
        param['style'] = '/static/css/styleForCurrentGame.css'

        cur_quest_id = data['current_games'][str(current_user.id)]['questions'][data['current_games'][str(current_user.id)]['current_question']]
        param['question'] = session.query(Question).filter(Question.id == cur_quest_id).first()

        temp_data = [0, 1, 2, 3]  # порядок вариантов
        shuffle(temp_data)  # рандомно изменяем его

        answers = param['question'].answers.split('!@#$%')
        shuffle_answers = []
        for x in temp_data:
            shuffle_answers.append(answers[x])

        param['answers'] = shuffle_answers

        param['current_number_quest'] = data['current_games'][str(current_user.id)]['current_question']

        if data['current_games'][str(current_user.id)]['quest_or_next'] == 'quest':
            param['title'] = 'Идёт игра'
            param['type_quest'] = random.choice(['change', 'write'])

            param['current_time'] = get_time() - data['current_games'][str(current_user.id)]['time']  # Разница между текущим и тем, когда началась игра

            param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()

            param['win'] = data['current_games'][str(current_user.id)]['wins']
            param['defeat'] = data['current_games'][str(current_user.id)]['defeats']

            param['path'] = f'/current_game'

            if request.method == 'GET':
                if param['current_time'] > 60:
                    user = session.query(User).filter(User.id == param['question'].who_add).first()
                    user.rating += 10
                    session.commit()

                    data['current_games'][str(current_user.id)]['quest_or_next'] = 'next'
                    save_json(data, 'static/json/games.json')

                    return redirect('/current_game')
                return render_template('current_game.html', **param)
            elif request.method == 'POST':
                data['current_games'][str(current_user.id)]['quest_or_next'] = 'next'
                save_json(data, 'static/json/games.json')
                if request.form.get('option'):
                    if request.form['option'].lower() in param['question'].right_answer.lower():
                        result = True
                    else:
                        result = False
                        user = session.query(User).filter(User.id == param['question'].who_add).first()
                        user.rating += 10
                        session.commit()
                else:
                    result = None
                data['current_games'][str(current_user.id)]['last_result'] = result
                if result:
                    data['current_games'][str(current_user.id)]['wins'] += 1
                else:
                    data['current_games'][str(current_user.id)]['defeats'] += 1
                save_json(data, 'static/json/games.json')
                return redirect(f'/current_game')
        else:
            param['title'] = 'Ответ'

            param['current_time'] = 0
            param['result'] = 'Вы ответили правильно' if data['current_games'][str(current_user.id)]['last_result'] else 'Вы не успели ответить' if data['current_games'][str(current_user.id)]['last_result'] is None else 'Вы ответили неправильно'

            param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()

            param['win'] = data['current_games'][str(current_user.id)]['wins']
            param['defeat'] = data['current_games'][str(current_user.id)]['defeats']

            if request.method == 'GET':
                return render_template('next_game.html', **param)
            elif request.method == 'POST':
                data['current_games'][str(current_user.id)]['quest_or_next'] = 'quest'
                data['current_games'][str(current_user.id)]['current_question'] += 1
                data['current_games'][str(current_user.id)]['time'] = get_time()
                save_json(data, 'static/json/games.json')
                if param['win'] != 6 and param['defeat'] != 6:
                    return redirect('/current_game')
                else:
                    if current_user.is_authenticated:
                        user = session.query(User).filter(User.id == current_user.id).first()
                        user.all_games += 1
                        user.wins += param['defeat'] != 6
                        user.defeats += param['win'] != 6
                        user.rating += 100 if param['defeat'] != 6 else param['win'] * 10

                        game_res = Game()
                        game_res.category = param['question'].category
                        game_res.result = param['defeat'] != 6
                        game_res.who_play = current_user.id
                        game_res.questions = '!@$'.join([str(x) for x in data['current_games'][str(current_user.id)]['questions']])
                        game_res.result_questions = f"{param['win']}:{param['defeat']}"
                        session.add(game_res)
                        session.commit()

                        data['current_games'][str(current_user.id)] = None
                        save_json(data, 'static/json/games.json')
                    return redirect('/end_game/200')
    else:
        return redirect('/login')


@app.route('/rating')
def rating():
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Рейтинг'
    param['style'] = '/static/css/styleForRating.css'
    all_users = session.query(User).all()
    all_users.sort(key=lambda x: (-x.rating, x.surname.lower() + x.name.lower(), x.nickname.lower()))
    param['users'] = all_users

    return render_template('rating.html', **param)


@app.route('/end_game/<why>')
def end_game(why):
    k = return_to_game()
    if k:
        return redirect('/current_game')
    param = {}

    param['title'] = 'Конец игры'
    param['style'] = '/static/css/styleForEndGame.css'
    if why == '404':
        param['why'] = 'Вы покинули страницу с вопросом и были дискфалифицированы'
    else:
        param['why'] = 'Результат записан'

    return render_template('end_game.html', **param)

#app.run(threaded=True)