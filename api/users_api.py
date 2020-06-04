from flask import Blueprint, jsonify, request
from data.users import User
from data import db_session
from werkzeug.security import generate_password_hash
from secondary_functions import get_time
import os


blueprint = Blueprint('users_api', __name__, template_folder='templates')

'''API для получения одного user'''
@blueprint.route('/api/123456789/user/<int:user_id>',  methods=['GET'])
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
@blueprint.route('/api/123456789/check_user',  methods=['POST'])
def check_user():
    session = db_session.create_session()
    user = session.query(User).filter(request.form['email'] == User.email).first()
    if not user:
        return jsonify({'errors': 'Неверный email или пароль'})
    if not user.check_password(request.form['psw']):
        return jsonify({'errors': 'Неверный email или пароль'})
    return jsonify({})


'''API для получения всех user'''
@blueprint.route('/api/123456789/users',  methods=['GET'])
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    if not users:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'nickname', 'email', 'password', 'rating', 'start_date', 'avatar',
                                   'link_vk', 'wins', 'defeats', 'add_questions', 'all_games', 'state'))
                 for item in users]
        }
    )


'''API для создания user'''
@blueprint.route('/api/123456789/add_user', methods=['POST'])
def create_user():

    if not request.form:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.form for key in
                 ['surname', 'name', 'nickname', 'email', 'password', 'password_again']):
        if request.form.get('surname'):
            return jsonify({'errors': 'Вы не ввели фамилию'})
        if request.form.get('name'):
            return jsonify({'errors': 'Вы не ввели имя'})
        if request.form.get('nickname'):
            return jsonify({'errors': 'Вы не ввели никнейм'})
        if request.form.get('email'):
            return jsonify({'errors': 'Вы не ввели почту'})
        if request.form.get('password'):
            return jsonify({'errors': 'Вы не ввели пароль'})
        if request.form.get('password_again'):
            return jsonify({'errors': 'Вы не ввели пароль ещё раз'})

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
            avatar=request.form['photo'] if request.form.get('photo') else '/static/img/users_avatars/no_photo.png',
            link_vk=request.form['link_vk'] if request.form.get('link_vk') else '',
            agree_newsletter=request.form['remember'] == 'on',
            wins=0,
            defeats=0,
            state='user',
            add_questions=0,
            all_games=0)
    except Exception:
        return jsonify({'errors': 'Неизвестная ошибка'})
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


'''API для удаления user'''
@blueprint.route('/api/123456789/delete_user/<int:user_id>', methods=['DELETE'])
def delete_questions(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


'''API для редактирования user'''
@blueprint.route('/api/123456789/put_user/<int:user_id>', methods=['PUT'])
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
        if request.files.get('image_' + str(user_id)):
            if user.avatar != '/static/img/users_avatars/no_photo.png':
                os.remove(user.avatar[1:])
            user.avatar = f'/static/img/users_avatars/{user.id}+{get_time()}.png'
            with open(user.avatar[1:], 'wb') as f1:  # 10
                f1.write(request.files['image_' + str(user_id)].read())
        session.commit()
    except Exception as e:
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})