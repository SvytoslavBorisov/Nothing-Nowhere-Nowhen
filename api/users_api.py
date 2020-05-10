from flask import Blueprint, jsonify, request
from data.users import User
from data import db_session
from werkzeug.security import generate_password_hash

blueprint = Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/12345/user/<int:user_id>',  methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user':
                user.to_dict(only=('id', 'surname', 'name', 'nickname', 'email', 'rating', 'start_date', 'avatar',
                                   'link_vk', 'wins', 'defeats', 'add_questions', 'all_games'))
        }
    )


@blueprint.route('/api/12345/users',  methods=['GET'])
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    if not users:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'nickname', 'email', 'rating', 'start_date', 'avatar',
                                   'link_vk', 'wins', 'defeats', 'add_questions', 'all_games'))
                 for item in users]
        }
    )


@blueprint.route('/api/12345/add_user', methods=['POST'])
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


@blueprint.route('/api/12345/delete_user/<int:user_id>', methods=['DELETE'])
def delete_questions(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    session.delete(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/12345/put_user/<int:user_id>', methods=['PUT'])
def put_questions(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    try:
        if request.json.get('surname'):
            user.surname = request.json['surname']
        if request.json.get('name'):
            user.name = request.json['name']
        if request.json.get('nickname'):
            user.nickname = request.json['nickname']
        if request.json.get('email'):
            user.email = request.json['email']
        if request.json.get('password'):
            user.password = request.json['password']

        session.commit()
    except:
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})