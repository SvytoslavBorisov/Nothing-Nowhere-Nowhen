from flask import Blueprint, jsonify, request
from data.questions import Question
from data import db_session


blueprint = Blueprint('questions_api', __name__, template_folder='templates')


'''API для получения одного вопроса'''
@blueprint.route('/api/123456789/question/<int:question_id>',  methods=['GET'])
def get_one_question(question_id):
    session = db_session.create_session()
    questions = session.query(Question).get(question_id)
    if not questions:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'question':
                questions.to_dict(only=('id', 'text', 'category.name', 'who_add.name', 'answers', 'right_answer', 'type', 'images'))
        }
    )


'''API для получения всех вопросов'''
@blueprint.route('/api/123456789/questions',  methods=['GET'])
def get_questions():
    session = db_session.create_session()
    questions = session.query(Question).all()
    if not questions:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'questions':
                [item.to_dict(only=('id', 'text', 'category.name', 'who_add.name', 'answers', 'right_answer', 'type', 'images'))
                 for item in questions]
        }
    )


'''API для создания вопроса'''
@blueprint.route('/api/123456789/add_quest', methods=['POST'])
def create_questions():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'text', 'category', 'answers', 'right_answer', 'who_add']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    quest = Question(
        id=request.json['id'],
        text=request.json['text'],
        category=request.json['category'],
        answers=request.json['answers'],
        right_answer=request.json['right_answer'],
        who_add=request.json['who_add']
    )
    session.add(quest)
    session.commit()
    return jsonify({'success': 'OK'})


'''API для удаления вопроса'''
@blueprint.route('/api/123456789/quests/<int:quest_id>', methods=['DELETE'])
def delete_questions(quest_id):
    session = db_session.create_session()
    quest = session.query(Question).get(quest_id)
    if not quest:
        return jsonify({'error': 'Not found'})
    session.delete(quest)
    session.commit()
    return jsonify({'success': 'OK'})


'''API для редактирования вопроса'''
@blueprint.route('/api/123456789/quests/<int:quest_id>', methods=['PUT'])
def put_questions(quest_id):
    session = db_session.create_session()
    quest = session.query(Question).get(quest_id)
    if not quest:
        return jsonify({'error': 'Not found'})

    try:
        if request.json.get('text'):
            quest.text = request.json['text']
        if request.json.get('category'):
            quest.category = request.json['category']
        if request.json.get('answers'):
            quest.answers = request.json['answers']
        if request.json.get('right_answer'):
            quest.right_answer = request.json['right_answer']
        if request.json.get('who_add'):
            quest.who_add = request.json['who_add']
        if request.json.get('is_promoted'):
            quest.is_promoted = request.json['is_promoted']

        session.commit()
    except:
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})