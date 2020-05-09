from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_restful import Api
from data import db_session
from requests import get, post, delete, put
from datetime import datetime
import datetime
import socket
import struct
import random
import json
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.categories import Category
from data.questions import Question
from data.users import User
from data.championship import Championship
from data.games import Game
from data.news import News
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.add_question import AddQuestionForm
from forms.check_quests import CheckQuestionForm
from random import choice, shuffle
from api import questions_resources, users_resources, questions_api


application = Flask(__name__)
application.config.update(
    JSON_AS_ASCII=False
)
api = Api(application)
login_manager = LoginManager()
login_manager.init_app(application)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/baseDate.sqlite")
application.register_blueprint(questions_api.blueprint)

api.add_resource(questions_resources.QuestionsListResource, '/api/questions')
api.add_resource(questions_resources.QuestionResource, '/api/question/<question_id>')

api.add_resource(users_resources.UsersListResource, '/api/users')
api.add_resource(users_resources.UserResource, '/api/user/<user_id>')


def get_bbox(GeoObject, k=0, k1=0, k2=0, k3=0):

    toponym_down_coords = list(map(float, GeoObject["boundedBy"]['Envelope']['lowerCorner'].split()))
    toponym_up_coords = list(map(float, GeoObject["boundedBy"]['Envelope']['upperCorner'].split()))

    return ",".join(
        [str(toponym_down_coords[0] + k), str(toponym_down_coords[1] + k1)]) + '~' + ",".join(
        [str(toponym_up_coords[0] + k2), str(toponym_up_coords[1] + k3)])


def open_json(file):
    with open(file, "r", errors='ignore') as f:
        return json.load(f)


def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@application.route('/categories')
def categories():
    if return_to_game():
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


@application.route('/', methods=['POST', 'GET'])
def main_page():
    if return_to_game():
        return redirect('/current_game')

    session = db_session.create_session()

    param = {}

    param['title'] = 'Главная страница'
    param['style'] = 'static/css/styleForMainPage.css'
    param['style_mobile'] = '/static/css_mobile/styleForMainPageMobile.css'

    param['news'] = [[x.text, x.image, x.caption] for x in session.query(News).all()]

    return render_template('main_page.html', **param)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route('/login', methods=['GET', 'POST'])
def login():
    if return_to_game():
        return redirect('/current_game')

    session = db_session.create_session()

    param = {}

    param['title'] = 'Вход'
    param['style'] = '/static/css/styleForLogin.css'
    param['style_mobile'] = '/static/css_mobile/styleForLoginMobile.css'
    param['script'] = ''

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/change_play')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, **param)
    return render_template('login.html', form=form, **param)


@application.route('/register', methods=['POST', 'GET'])
def register():
    if return_to_game():
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


@application.route('/user_info/<string:user>')
def user_info(user):
    k = return_to_game()
    if k:
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Профиль'
    param['style'] = '/static/css/styleForUserInfo.css'
    param['style_mobile'] = '/static/css_mobile/styleForUserInfoMobile.css'
    param['user'] = session.query(User).filter(User.nickname == user).first()
    param['games'] = param['user'].games
    if param['user'].all_games:
        param['procent_win'] = int((param['user'].wins / param['user'].all_games) * 100)
        param['procent_def'] = int(100 - param['procent_win'])
    else:
        param['procent_win'] = 50
        param['procent_def'] = 50

    return render_template('user_info.html', **param)


@application.route('/add_question/<string:user>', methods=['POST', 'GET'])
@login_required
def add_question(user):
    if return_to_game():
        return redirect('/current_game')

    session = db_session.create_session()
    param = {}

    param['title'] = 'Создать вопрос'
    param['style'] = '/static/css/styleForAddQuestion.css'
    param['categories'] = session.query(Category).all()

    form = AddQuestionForm()
    form.category.choices = [(x.name, x.name) for x in param['categories'][1:]]
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


@application.route('/about_site', methods=['POST', 'GET'])
def about_site():

    if return_to_game():
        return redirect('/current_game')
    param = {}

    param['title'] = 'О сайте'
    param['style'] = '/static/css/styleForAboutSite.css'
    param['style_mobile'] = '/static/css_mobile/styleForAboutSiteMobile.css'
    return render_template('about_site.html', **param)


@application.route('/game/<int:id_>', methods=['POST', 'GET'])
def game(id_):

    if return_to_game():
        return redirect('/current_game')
    session = db_session.create_session()

    param = {}

    param['title'] = 'Начать игру'
    param['style'] = '/static/css/styleForGame.css'
    param['category'] = session.query(Category).filter(Category.id == id_).first()

    if request.method == 'GET':
        return render_template('game.html', **param)
    elif request.method == 'POST':

        return redirect(f'/start_game/{str(id_)}+{str(request.form["complexity"])}+{str(request.form["type"])}')


@application.route('/start_game/<int:id_>+<int:comp_>+<type>')
def start_game(id_, comp_, type):

    if return_to_game():
        return redirect('/current_game')
    session = db_session.create_session()

    quests = []
    if current_user.is_authenticated:
        if id_ != 1:
            for question in session.query(Question).filter(Question.category == id_, Question.who_add != current_user.id, (Question.type == type) | (Question.type == 'all'), Question.complexity == int(comp_)):
                quests.append(question)
        else:
            for question in session.query(Question).filter(Question.who_add != current_user.id, Question.complexity == int(comp_)):
                quests.append(question)
    else:
        if id_ != 1:
            for question in session.query(Question).filter(Question.category == id_, (Question.type == type) | (Question.type == 'all'), Question.complexity == int(comp_)):
                quests.append(question)
        else:
            for question in session.query(Question):
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
            'category': id_,
            'defeats': 0,
            'current_question': 0,
            'time': get_time(),
            'quest_or_next': 'quest',
            'last_result': None,
            'type': type,
            'complexity': comp_,
            'last_answer': '',
            'delete': [],
            'create_map': 'yes'
        }
        data['current_games'][str(current_user.id)] = {}
        for x in load:
            data['current_games'][str(current_user.id)][x] = load[x]
        print(0)
        print(data)
        save_json(data, 'static/json/games.json')

    return redirect('/current_game')


@application.route('/current_game', methods=['POST', 'GET'])
def current_game():
    session = db_session.create_session()
    if current_user.is_authenticated:
        data = open_json('static/json/games.json')

        if not data['current_games'][str(current_user.id)]:
            return redirect('/change_play')

        param = {}
        param['style'] = '/static/css/styleForCurrentGame.css'
        param['style_mobile'] = '/static/css_mobile/styleForCurrentGameMobile.css'

        cur_quest_id = data['current_games'][str(current_user.id)]['questions'][data['current_games'][str(current_user.id)]['current_question']]
        param['question'] = session.query(Question).filter(Question.id == cur_quest_id).first()

        temp_data = [0, 1, 2, 3]  # порядок вариантов
        shuffle(temp_data)        # рандомно изменяем его

        answers = param['question'].answers.split('!@#$%')
        shuffle_answers = []
        for x in temp_data:
            shuffle_answers.append(answers[x])

        param['answers'] = shuffle_answers
        param['current_number_quest'] = data['current_games'][str(current_user.id)]['current_question']

        if data['current_games'][str(current_user.id)]['quest_or_next'] == 'quest':

            if param['question'].images.split('!@#')[0] == 'map':
                param['image_type'] = 'map'
            else:
                param['image_question'] = param['question'].images
                param['image_type'] = ''

            if param['question'].images.split('!@#')[0] == 'map' and data['current_games'][str(current_user.id)]['create_map']:
                temp_data = param['question'].images.split('!@#')

                coord_map = [float(x) for x in temp_data[3].split(', ')]
                coord_sat = [float(x) for x in temp_data[2].split(', ')]
                toponym_to_find = temp_data[1]

                geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

                geocoder_params = {
                    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                    "geocode": toponym_to_find,
                    "format": "json"}

                response = get(geocoder_api_server, params=geocoder_params)

                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]

                toponym_coodrinates = toponym["Point"]["pos"]
                toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

                type_map = random.choice([0, 1])

                if type_map:
                    typeMap = 'map'
                    coord = coord_map
                else:
                    typeMap = 'sat'
                    coord = coord_sat

                map_params = {
                    "ll": ",".join([toponym_longitude, toponym_lattitude]),
                    "l": typeMap,
                    'bbox': get_bbox(toponym, k=coord[0], k1=coord[1], k2=coord[2], k3=coord[3])
                }

                map_api_server = "http://static-maps.yandex.ru/1.x/"
                response = get(map_api_server, params=map_params)

                image_path = f'static/img/questions/{get_time()}+{current_user.id}.png'
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                param['image_question'] = image_path
                data['current_games'][str(current_user.id)]['delete'].append(image_path)
                data['current_games'][str(current_user.id)]['create_map'] =  None
                save_json(data, 'static/json/games.json')

            param['title'] = 'Идёт игра'
            param['type_quest'] = data['current_games'][str(current_user.id)]['type']

            param['current_time'] = get_time() - data['current_games'][str(current_user.id)]['time']  # Разница между текущим и тем, когда началась игра

            param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()

            param['win'] = data['current_games'][str(current_user.id)]['wins']
            param['defeat'] = data['current_games'][str(current_user.id)]['defeats']

            param['path'] = f'/current_game'

            if request.method == 'GET':
                if param['current_time'] > 60:
                    data['current_games'][str(current_user.id)]['quest_or_next'] = 'next'
                    save_json(data, 'static/json/games.json')
                    if request.form.get('option'):
                        if request.form['option'].lower().strip().replace('ё', 'е') in set([x.lower().strip() for x in param['question'].right_answer.split('!@#$%')]):
                            result = True
                        else:
                            result = False
                            user = session.query(User).filter(User.id == param['question'].who_add).first()
                            user.rating += 1
                            session.commit()
                    else:
                        result = False
                        user = session.query(User).filter(User.id == param['question'].who_add).first()
                        user.rating += 1
                        session.commit()
                    data['current_games'][str(current_user.id)]['last_result'] = result
                    if result:
                        data['current_games'][str(current_user.id)]['wins'] += 1
                    else:
                        data['current_games'][str(current_user.id)]['defeats'] += 1
                    save_json(data, 'static/json/games.json')

                    data['current_games'][str(current_user.id)]['last_answer'] = request.form.get('option') if request.form.get('option') else ' '
                    return redirect(f'/current_game')
                print(param['image_type'])
                return render_template('current_game.html', **param)
            elif request.method == 'POST':
                data['current_games'][str(current_user.id)]['quest_or_next'] = 'next'
                save_json(data, 'static/json/games.json')
                if request.form.get('option'):
                    if request.form['option'].lower().strip().replace('ё', 'е') in set([x.lower().strip() for x in param['question'].right_answer.split('!@#$%')]):
                        result = True
                    else:
                        result = False
                        user = session.query(User).filter(User.id == param['question'].who_add).first()
                        user.rating += 1
                        session.commit()
                else:
                    result = None
                data['current_games'][str(current_user.id)]['last_result'] = result
                data['current_games'][str(current_user.id)]['last_answer'] = request.form.get('option') if request.form.get('option') else ' '
                if result:
                    data['current_games'][str(current_user.id)]['wins'] += 1
                else:
                    data['current_games'][str(current_user.id)]['defeats'] += 1
                save_json(data, 'static/json/games.json')
                return redirect(f'/current_game')
        else:
            param['title'] = 'Ответ'

            if param['question'].images.split('!@#')[0] == 'map':
                param['image_question'] = data['current_games'][str(current_user.id)]['delete'][-1]
                param['image_type'] = 'map'
            else:
                param['image_question'] = param['question'].images
                param['image_type'] = ''

            param['current_time'] = 0
            param['result'] = 'Вы ответили правильно' if data['current_games'][str(current_user.id)]['last_result'] else 'Вы ответили неправильно'

            param['user'] = session.query(User).filter(User.id == param['question'].who_add).first()

            param['win'] = data['current_games'][str(current_user.id)]['wins']
            param['defeat'] = data['current_games'][str(current_user.id)]['defeats']

            param['last_answer'] = data['current_games'][str(current_user.id)]['last_answer']

            if request.method == 'GET':
                return render_template('next_game.html', **param)
            elif request.method == 'POST':
                data['current_games'][str(current_user.id)]['quest_or_next'] = 'quest'
                data['current_games'][str(current_user.id)]['current_question'] += 1
                data['current_games'][str(current_user.id)]['time'] = get_time()
                data['current_games'][str(current_user.id)]['create_map'] = 'yes'
                save_json(data, 'static/json/games.json')
                if param['win'] != 6 and param['defeat'] != 6:
                    return redirect('/current_game')
                else:
                    if current_user.is_authenticated:
                        user = session.query(User).filter(User.id == current_user.id).first()
                        user.all_games += 1
                        user.wins += param['defeat'] != 6
                        user.defeats += param['win'] != 6
                        user.rating += 20 * int(data['current_games'][str(current_user.id)]['complexity']) if param['defeat'] != 6 else param['win'] * int(data['current_games'][str(current_user.id)]['complexity'])

                        game_res = Game()
                        game_res.category = param['question'].category
                        game_res.result = param['defeat'] != 6
                        game_res.who_play = current_user.id
                        game_res.questions = '!@$'.join([str(x) for x in data['current_games'][str(current_user.id)]['questions']])
                        game_res.result_questions = f"{param['win']}:{param['defeat']}"
                        session.add(game_res)
                        session.commit()

                        for x in data['current_games'][str(current_user.id)]['delete']:
                            os.remove(x)
                        data['current_games'][str(current_user.id)] = None

                        save_json(data, 'static/json/games.json')
                    return redirect('/end_game/200')
    else:
        return redirect('/login')


@application.route('/rating')
def rating():

    if return_to_game():
        return redirect('/current_game')
    session = db_session.create_session()
    param = {}

    param['title'] = 'Рейтинг'
    param['style'] = '/static/css/styleForRating.css'
    param['style_mobile'] = '/static/css_mobile/styleForRatingMobile.css'
    all_users = session.query(User).all()
    all_users.sort(key=lambda x: (-x.rating, x.surname.lower() + x.name.lower(), x.nickname.lower()))
    param['users'] = all_users

    return render_template('rating.html', **param)


@application.route('/end_game/<why>')
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


@application.route('/check_quests', methods=['POST', 'GET'])
def check_quests():
    if return_to_game():
        return redirect('/current_game')

    form = CheckQuestionForm()
    if current_user.is_authenticated and current_user.state == 'admin':

        session = db_session.create_session()

        if request.method == 'POST':
            if request.form.get('submit'):
                question = session.query(Question).filter(Question.is_promoted == 0).first()

                question.text = request.form['text']
                question.category = session.query(Category).filter(Category.name == request.form['category']).first().id
                question.answers = "!@#$%".join(
                    [request.form['answer'], request.form['wrong_answer1'], request.form['wrong_answer2'],
                     request.form['wrong_answer3']])
                question.right_answer = request.form['answer']
                question.is_promoted = True
                question.comment = request.form['comment']
                question.type = request.form['type']
                question.comp = request.form['comp']

                session.add(question)
                session.commit()
            else:
                question = session.query(Question).filter(Question.is_promoted == 0).first()
                session.delete(question)
                session.commit()

        param = {}

        param['title'] = 'Просмотр вопросов'
        param['style'] = '/static/css/styleForCheckQuests.css'

        param['categories'] = session.query(Category).all()
        param['quest'] = session.query(Question).filter(Question.is_promoted == 0).first()

        if param['quest']:
            temp = param['quest'].answers.split('!@#$%')
            form.text.default = param['quest'].text
            form.answer.default = temp[0]
            form.comment.default = param['quest'].comment
            form.category.choices = [(x.name, x.name) for x in param['categories'][1:]]
            form.category.default = param['quest'].orm_with_category.name
            form.wrong_answer1.default = temp[1]
            form.wrong_answer2.default = temp[2]
            form.wrong_answer3.default = temp[3]
            return render_template('check_quests.html', form=form, **param)
        else:
            return redirect('/user_info/' + current_user.nickname)
    else:
        return redirect('/login')


@application.route('/championship/<int:id_>', methods=['POST', 'GET'])
def championship(id_):

    if  return_to_game():
        return redirect('/current_game')

    if request.method == 'GET':
        param = {}

        param['title'] = 'Чемпионат'
        param['style'] = '/static/css/styleForChampionshipStart.css'
        session = db_session.create_session()

        param['championship'] = session.query(Championship).filter(Championship.id == id_).first()
        return render_template('championship_start.html', **param)
    elif request.method == 'POST':
        return redirect(f'/championship_start/{str(id_)}')


@application.route('/championship_start/<int:id_>')
def start_championship(id_):

    if return_to_game():
        return redirect('/current_game')

    session = db_session.create_session()

    param = {}

    param['title'] = 'Начать чемпионат'
    param['style'] = '/static/css/styleForCheckQuests.css'

    param['championship'] = session.query(Championship).filter(Championship.id == id_).first()

    selected = param['championship'].members.split('!@#$%')
    selected_images = param['championship'].images.split('!@#$%')
    all_selected = {selected[i] : f'/static/img/championships/{id_}/' + selected_images[i] + '.png' for i in range(len(selected))}
    shuffle(selected)

    if current_user.is_authenticated:
        data = open_json('static/json/championships.json')
        load = {
            'id': param['championship'].id,
            'members': selected,
            'images': all_selected,
            'all_stage': param['championship'].type,
            'current_stage': param['championship'].type,
            'stage': 0,
            'delete': []
        }
        data['current_championships'][str(current_user.id)] = {}
        for x in load:
            data['current_championships'][str(current_user.id)][x] = load[x]
        save_json(data, 'static/json/championships.json')

        return redirect('/championship_game')
    return redirect('/login')


@application.route('/championships')
def championships():

    if return_to_game():
        return redirect('/current_game')

    param = {}

    param['title'] = 'Чемпионаты'
    param['style'] = '/static/css/styleForChampionships.css'
    session = db_session.create_session()

    param['championships'] = session.query(Championship).all()

    return render_template('championships.html', **param)


@application.route('/championship_game', methods=['POST', 'GET'])
def current_championship():

    if request.method == 'GET':
        if current_user.is_authenticated:
            data = open_json('static/json/championships.json')

            param = {}
            param['style'] = '/static/css/styleForChampionshipGame.css'
            #param['style_mobile'] = '/static/css_mobile/styleForCurrentGameMobile.css'

            param['first'] = data['current_championships'][str(current_user.id)]['members'][data['current_championships'][str(current_user.id)]['stage'] * 2]
            param['first_img'] = data['current_championships'][str(current_user.id)]['images'][param['first']]
            param['second'] = data['current_championships'][str(current_user.id)]['members'][data['current_championships'][str(current_user.id)]['stage'] * 2 + 1]
            param['second_img'] = data['current_championships'][str(current_user.id)]['images'][param['second']]

            param['curr_stage_number'] = data['current_championships'][str(current_user.id)]['current_stage']
            if param['curr_stage_number'] == 2:
                param['curr_stage'] = 'Полуфинал'
            elif param['curr_stage_number'] == 4:
                param['curr_stage'] = 'Четвертьфинал'
            elif param['curr_stage_number'] == 1:
                param['curr_stage'] = 'Финал'
            else:
                param['curr_stage'] = f'1 / {param["curr_stage_number"]}'
            param['stage'] = data['current_championships'][str(current_user.id)]['stage']

            return render_template('championship_game.html', **param)
    elif request.method == 'POST':
        data = open_json('static/json/championships.json')
        if request.form.get('first') != None:
            print('Вы проголосовали за ', data['current_championships'][str(current_user.id)]['members'][data['current_championships'][str(current_user.id)]['stage'] * 2])
            data['current_championships'][str(current_user.id)]['delete'].append(
                data['current_championships'][str(current_user.id)]['members'][
                    data['current_championships'][str(current_user.id)]['stage'] * 2 + 1])
        else:
            print('Вы проголосовали за ', data['current_championships'][str(current_user.id)]['members'][data['current_championships'][str(current_user.id)]['stage'] * 2 + 1])
            data['current_championships'][str(current_user.id)]['delete'].append(
                data['current_championships'][str(current_user.id)]['members'][
                    data['current_championships'][str(current_user.id)]['stage'] * 2])
        data['current_championships'][str(current_user.id)]['stage'] += 1
        save_json(data, 'static/json/championships.json')

        if data['current_championships'][str(current_user.id)]['current_stage'] == 1:
            data['current_championships'][str(current_user.id)]['members'].remove(data['current_championships'][str(current_user.id)]['delete'][-1])
            save_json(data, 'static/json/championships.json')

            session = db_session.create_session()

            championship = session.query(Championship).filter(Championship.id == data['current_championships'][str(current_user.id)]['id']).first()
            championship_members = championship.members.split('!@#$%')

            temp = championship.procent.split('!@#$%')
            temp[championship_members.index(data['current_championships'][str(current_user.id)]['members'][0])] = int(temp[championship_members.index(data['current_championships'][str(current_user.id)]['members'][0])])
            temp[championship_members.index(data['current_championships'][str(current_user.id)]['members'][0])] += 1
            championship.procent = '!@#$%'.join([str(x) for x in temp])

            championship.games += 1

            session.commit()
            return redirect('/championship_end')

        if data['current_championships'][str(current_user.id)]['stage'] == data['current_championships'][str(current_user.id)]['current_stage']:
            for x in data['current_championships'][str(current_user.id)]['delete']:
                if x in data['current_championships'][str(current_user.id)]['members']:
                    data['current_championships'][str(current_user.id)]['members'].remove(x)
            data['current_championships'][str(current_user.id)]['stage'] = 0
            data['current_championships'][str(current_user.id)]['current_stage'] = data['current_championships'][str(current_user.id)]['current_stage'] // 2
            shuffle(data['current_championships'][str(current_user.id)]['members'])
        save_json(data, 'static/json/championships.json')
        return redirect('/championship_game')


@application.route('/championship_end', methods=['POST', 'GET'])
def championship_end():
    if current_user.is_authenticated:
        data = open_json('static/json/championships.json')

        param = {}
        param['style'] = '/static/css/styleForChampionshipEnd.css'
        param['win'] = data['current_championships'][str(current_user.id)]['members'][0]
        param['img'] = data['current_championships'][str(current_user.id)]['images'][param['win']]
        param['id'] = data['current_championships'][str(current_user.id)]['id']
        return render_template('championship_end.html', **param)
    return redirect('/login')


@application.route('/championship_rating/<int:id_>', methods=['POST', 'GET'])
def championship_rating(id_):
    if current_user.is_authenticated:
        data = open_json('static/json/championships.json')

        data['current_championships'][str(current_user.id)] = None

        save_json(data, 'static/json/championships.json')

        session = db_session.create_session()

        championship = session.query(Championship).filter(
            Championship.id == id_).first()

        param = {}
        param['style'] = '/static/css/styleForChampionshipRating.css'
        param['title'] = 'Рейтинг чеспионата'
        param['title1'] = championship.title
        param['procent'] = championship.procent.split('!@#$%')
        param['members'] = championship.members.split('!@#$%')
        param['all_games'] = championship.games

        param['players'] = [[param['members'][i], str((int(param['procent'][i]) * 100) / int(param['all_games']))] for i in range(len(param['members']))]
        param['players'].sort(key=lambda x: float(x[1]), reverse=True)

        return render_template('championship_rating.html', **param)
    return redirect('/login')


@application.route('/change_play/')
def change_play():
    param = {}
    param['style'] = '/static/css/styleForChangePlay.css'
    param['title'] = 'Выбор игры'
    return render_template('change_play.html', **param)


#application.run()