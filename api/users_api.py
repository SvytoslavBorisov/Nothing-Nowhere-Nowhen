from flask import Blueprint, jsonify, request
from data.users import User
from data import db_session
from werkzeug.security import generate_password_hash
from secondary_functions import get_time
import os
import configparser

'''Cоздаём объекта парсера. Читаем конфигурационный файл'''
config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

"""Загрузка переменных среды из файла"""
from dotenv import load_dotenv
load_dotenv(dotenv_path=config['PATH']['SECRET_DATA'])


blueprint = Blueprint('users_api', __name__, template_folder='templates')

'''API для получения одного user'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/user/<int:user_id>',  methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user':
                user.to_dict(only=('id', 'surname', 'name', 'nickname', 'email', 'password', 'rating', 'start_date', 'avatar',
                                   'link_vk', 'wins', 'defeats', 'add_questions', 'all_games', 'state'))
        }
    )

'''API для проверки введенных данных'''
@blueprint.route(f'/api/check_user',  methods=['POST'])
def check_user():
    session = db_session.create_session()
    user = session.query(User).filter(request.form['email'] == User.email).first()
    if not user:
        return jsonify({'errors': 'Неверный email или пароль'})
    if not user.check_password(request.form['psw']):
        return jsonify({'errors': 'Неверный email или пароль'})
    return jsonify({})


'''API для получения всех user'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/users',  methods=['GET'])
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    if not users:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'nickname', 'email', 'password', 'rating', 'start_date', 'avatar',
                                   'link_vk', 'wins', 'defeats', 'add_questions', 'all_games', 'state', 'agree_newsletter'))
                 for item in users]
        }
    )


'''API для создания user'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/add_user', methods=['POST'])
def create_user():

    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == request.form['email']).first()  # 7
        if user:
            return jsonify({'errors': 'Email уже используется'})
        user = session.query(User).filter(User.nickname == request.form['nickname']).first()  # 7
        if user:
            return jsonify({'errors': 'Никнейм уже используется'})
        user = User(
            surname=request.form['surname'],
            name=request.form['name'],
            nickname=request.form['nickname'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password']),
            rating=0,
            link_vk=request.form['link_vk'] if request.form.get('link_vk') else '',
            agree_newsletter=1 if request.form.get('remember') else 0,
            wins=0,
            defeats=0,
            state='user',
            add_questions=0,
            all_games=0)

        session.add(user)
        session.commit()

        file = request.files['photo'].read()
        if str(file) != "b''":
            file = request.files['photo'].read()
            user.avatar = f'/static/img/users_avatars/{user.id}+{get_time()}.png'
            with open(user.avatar[1:], 'wb') as f1:  # 10
                f1.write(file)
        else:
            user.avatar = '/static/img/users_avatars/ no_photo.png'
    except Exception:
        return jsonify({'errors': 'Неизвестная ошибка'})
    session.commit()
    return jsonify({'success': 'OK'})


'''API для удаления user'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/delete_user/<int:user_id>', methods=['DELETE'])
def delete_questions(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


'''API для редактирования user'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/put_user/<int:user_id>', methods=['PUT'])
def put_questions(user_id):

    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    try:
        if request.form.get('nick_' + str(user_id)):
            user.nickname = request.form['nick_' + str(user_id)].strip()
        if request.form.get('name_' + str(user_id)):
            user.name = request.form['name_' + str(user_id)].strip()
        if request.form.get('surname_' + str(user_id)):
            user.surname = request.form['surname_' + str(user_id)].strip()
        if request.form.get('email_' + str(user_id)):
            user.email = request.form['email_' + str(user_id)].strip()
        if request.form.get('link_vk_' + str(user_id)):
            user.link_vk = request.form['link_vk_' + str(user_id)].strip()
        if request.form.get('rating_' + str(user_id)):
            user.rating = request.form['rating_' + str(user_id)].strip()
        if request.form.get('all_games_' + str(user_id)):
            user.all_games = request.form['all_games_' + str(user_id)].strip()
        if request.form.get('wins_' + str(user_id)):
            user.wins = request.form['wins_' + str(user_id)].strip()
        if request.form.get('defeats_' + str(user_id)):
            user.defeats = request.form['defeats_' + str(user_id)].strip()
        if request.form.get('select_type_users_edit_redactor_' + str(user_id)):
            user.state = request.form['select_type_users_edit_redactor_' + str(user_id)]
        if request.form.get('remember_' + str(user_id)):
            user.agree_newsletter = 1
        else:
            user.agree_newsletter = 0
        if request.files.get('image_' + str(user_id)):
            file = request.files['image_' + str(user_id)].read()
            if str(file) != "b''":
                if user.avatar != '/static/img/users_avatars/no_photo.png':
                    os.remove(user.avatar[1:])
                user.avatar = f'/static/img/users_avatars/{user.id}+{get_time()}.png'
                with open(user.avatar[1:], 'wb') as f1:  # 10
                    f1.write(file)
        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})