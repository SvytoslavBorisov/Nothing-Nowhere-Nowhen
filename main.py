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
from api import questions_resources#, questions_api


app = Flask(__name__)
app.config.update(
    JSON_AS_ASCII=False
)
api = Api(app)
#app.register_blueprint(questions_api.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")
api.add_resource(questions_resources.QuestionsListResource, '/api/questions')
api.add_resource(questions_resources.QuestionResource, '/api/question/<question_id>')


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
    session = db_session.create_session()

    param = {}

    param['title'] = 'Играть'
    param['style'] = '/static/css/styleForCategories.css'
    param['script'] = ''
    param['categories'] = session.query(Category).all()

    if request.method == 'GET':
        return render_template('categories.html', **param)
    elif request.method == 'POST':
        return render_template('categories.html', **param)


@app.route('/', methods=['POST', 'GET'])
def main_page():
    param = {}

    param['title'] = 'Главная страница'
    param['style'] = 'static/css/styleForMainPage.css'
    return render_template('main_page.html', **param)


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
    global cipher
    session = db_session.create_session()

    quests = []
    for question in session.query(Question).filter(Question.category == id_, Question.who_add != current_user.id):
        quests.append(question)

    selected = []
    for _ in range(min(len(quests), 11)):
        k = choice(quests)
        while k in selected:
            k = choice(quests)
        selected.append(k)

    temp_data = ['0', '1', '2', '3']  # порядок вариантов
    shuffle(temp_data)  # рандомно изменяем его

    text = bytes(f'{"!@$".join([str(x.id) for x in selected])}'  # id вопросов, которые будут в игре
                f'{"!@$" + "0"}'  # сколько игрок правильно ответил
                f'{"!@$" + "".join(temp_data)}'  # порядок вариантов ответов
                f'{"!@$" + "0"}'  # номер текущего вопроса
                f'{"!@$" + str(get_time())}', encoding='UTF-8')  # текущее время из интернета

    cipher_key = Fernet.generate_key()
    cipher = Fernet(cipher_key)
    encrypted_text = cipher.encrypt(text)

    return redirect(f'/current_game/{str(encrypted_text)[2:-1]}')


@app.route('/current_game/<quests_hash>', methods=['POST', 'GET'])
def current_game(quests_hash):
    global cipher
    session = db_session.create_session()
    try:
        quests = str(cipher.decrypt(bytes(quests_hash, encoding='UTF-8')))[2:-1]
    except Exception as e:
        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)
        return redirect('/end_game/404')

    data_from_path = quests.split('!@$')

    param = {}

    param['title'] = 'Идёт игра'
    param['style'] = '/static/css/styleForCurrentGame.css'

    count_right_answers = int(data_from_path[-4])

    param['current_time'] = get_time() - int(data_from_path[-1])  # Разница между текущим и тем, когда началась игра

    param['question'] = session.query(Question).filter(Question.id == int(data_from_path[int(data_from_path[-2])])).first()
    param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()

    param['answers'] = ['', '', '', '']
    for i in range(4):
        param['answers'][i] = param['question'].answers.split('!@#$%')[int(data_from_path[-3][i])]
    """
       Для каждого ответа заранее заготовлен номер ячейки, где он будет находиться
    """

    param['current_number_quest'] = int(data_from_path[-2])

    param['win'] = count_right_answers
    param['defeat'] = int(data_from_path[-2]) - count_right_answers

    questions = data_from_path[:-4]

    param['path'] = quests_hash

    if request.method == 'GET':
        if param['current_time'] > 60:  # Время на вопрос закончилось

            cipher_key = Fernet.generate_key()
            cipher = Fernet(cipher_key)

            user = session.query(User).filter(User.id == param['question'].who_add).first()
            user.rating += 10
            session.commit()

            text = bytes(f'{"!@$".join([x for x in questions])}'
                         f'{"!@$" + str(count_right_answers)}'
                         f'{"!@$" + data_from_path[-3]}'
                         f'{"!@$" + str(param["current_number_quest"])}'
                         f'{"!@$" + "time"}', encoding='UTF-8')

            encrypted_text = cipher.encrypt(text)
            return redirect(f'/next_quest/{str(encrypted_text)[2:-1]}')
        return render_template('current_game.html', **param)
    elif request.method == 'POST':
        if request.form.get('option'):
            if request.form['option'] == param['question'].right_answer:
                result = True
            else:
                result = False
                user = session.query(User).filter(User.id == param['question'].who_add).first()
                user.rating += 10
                session.commit()
        else:
            result = False

        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)

        text = bytes(f'{"!@$".join([x for x in questions])}'
                     f'{"!@$" + str(count_right_answers)}'
                     f'{"!@$" + data_from_path[-3]}'
                     f'{"!@$" + str(param["current_number_quest"])}'
                     f'{"!@$" + str(result)}', encoding='UTF-8')

        encrypted_text = cipher.encrypt(text)

        return redirect(f'/next_quest/{str(encrypted_text)[2:-1]}')


@app.route('/next_quest/<quests_hash>', methods=['POST', 'GET'])
def next_quest(quests_hash):
    global cipher
    session = db_session.create_session()
    try:
        quests = str(cipher.decrypt(bytes(quests_hash, encoding='UTF-8')))[2:-1]
    except Exception as e:
        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)
        return redirect('/end_game/404')

    param = {}
    param['title'] = 'Ответ'
    param['style'] = '/static/css/styleForCurrentGame.css'

    data_from_path = quests.split('!@$')
    param['result'] = 'Вы ответили правильно' if data_from_path[-1] == 'True' \
        else 'Вы не успели ответить' if data_from_path[-1] == 'time' else 'Вы ответили неправильно'

    param['question'] = session.query(Question).filter(
        Question.id == int(data_from_path[int(data_from_path[-2])])).first()
    param['current_number_quest'] = int(data_from_path[-2])

    count_right_answers = int(data_from_path[-4])
    if data_from_path[-1] == 'True':
        count_right_answers += 1

    param['answers'] = ['', '', '', '']
    for i in range(4):
        param['answers'][i] = param['question'].answers.split('!@#$%')[int(data_from_path[-3][i])]

    param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()

    param['win'] = count_right_answers
    param['defeat'] = int(data_from_path[-2]) - count_right_answers + 1

    questions = data_from_path[:-4]

    if request.method == 'GET':
        return render_template('next_game.html', **param)
    elif request.method == 'POST':

        temp_data = ['0', '1', '2', '3']  # порядок вариантов
        shuffle(temp_data)

        if param['win'] != 6 and param['defeat'] != 6:

            cipher_key = Fernet.generate_key()
            cipher = Fernet(cipher_key)

            text = bytes(f'{"!@$".join([x for x in questions])}'
                         f'{"!@$" + str(count_right_answers)}'
                         f'{"!@$" + "".join(temp_data)}'
                         f'{"!@$" + str(param["current_number_quest"] + 1)}'
                         f'{"!@$" + str(get_time())}', encoding='UTF-8')

            encrypted_text = cipher.encrypt(text)

            return redirect(f'/current_game/{str(encrypted_text)[2:-1]}')
        else:
            cipher_key = Fernet.generate_key()
            cipher = Fernet(cipher_key)

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
                game_res.questions = '!@$'.join(data_from_path[0:-4])
                game_res.result_questions = f"{param['win']}:{param['defeat']}"
                session.add(game_res)
                session.commit()

            return redirect('/end_game/200')


@app.route('/rating')
def rating():
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
    param = {}

    param['title'] = 'Конец игры'
    param['style'] = '/static/css/styleForEndGame.css'
    if why == '404':
        param['why'] = 'Вы покинули страницу с вопросом и были дискфалифицированы'
    else:
        param['why'] = 'Результат записан'

    return render_template('end_game.html', **param)


cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)
