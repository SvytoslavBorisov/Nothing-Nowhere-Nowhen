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
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'nickname', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    try:
        user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        nickname=request.json['nickname'],
        email=request.json['email'],
        password=generate_password_hash(request.json['password']),
        rating=0,
        avatar='',
        link_vk='',
        wins=0,
        defeats=0,
        add_questions=0,
        all_games=0)
    except Exception:
        return jsonify({'success': 'id занят'})
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
            print(1)
            user.nickname = request.form['nick_' + str(user_id)].strip()
        if request.form.get('name_' + str(user_id)):
            print(2)
            user.name = request.form['name_' + str(user_id)].strip()
        if request.form.get('surname_' + str(user_id)):
            print(3)
            user.surname = request.form['surname_' + str(user_id)].strip()
        if request.form.get('email_' + str(user_id)):
            print(4)
            user.email = request.form['email_' + str(user_id)].strip()
        if request.form.get('link_vk_' + str(user_id)):
            print(5)
            user.link_vk = request.form['link_vk_' + str(user_id)].strip()

        if request.form.get('rating_' + str(user_id)):
            print(6)
            user.rating = request.form['rating_' + str(user_id)].strip()
        if request.form.get('all_games_' + str(user_id)):
            print(7)
            user.all_games = request.form['all_games_' + str(user_id)].strip()
        if request.form.get('wins_' + str(user_id)):
            print(8)
            user.wins = request.form['wins_' + str(user_id)].strip()
        if request.form.get('defeats_' + str(user_id)):
            print(9)
            user.defeats = request.form['defeats_' + str(user_id)].strip()
        if request.form.get('select_type_users_edit_redactor_' + str(user_id)):
            print(11)
            user.state = request.form['select_type_users_edit_redactor_' + str(user_id)]
        if request.files.get('image_' + str(user_id)):
            print(12)
            if user.avatar != '/static/img/users_avatars/no_photo.png':
                os.remove(user.avatar[1:])
            user.avatar = f'/static/img/users_avatars/{user.id}+{get_time()}.png'
            with open(user.avatar[1:], 'wb') as f1:  # 10
                f1.write(request.files['image_' + str(user_id)].read())
        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})