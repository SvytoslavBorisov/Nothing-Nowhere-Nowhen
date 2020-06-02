from flask import Blueprint, jsonify, request
from data.questions import Question
from data.categories import Category
from data import db_session
import os
from secondary_functions import get_time


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
                questions.to_dict(only=('id', 'text', 'category.name', 'who_add.name', 'answers', 'right_answer', 'type', 'images', 'complexity'))
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
                [{'id': item.id,
                  'text': item.text,
                  'category': item.orm_with_category.name,
                  'who_add': item.orm_with_users.nickname,
                  'answers': item.answers,
                  'right_answer': item.right_answer,
                  'type': item.type,
                  'images': item.images,
                  'complexity': item.complexity} for item in questions]
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
        if request.form.get('text_' + str(quest_id)):
            print(1)
            quest.text = request.form['text_' + str(quest_id)].strip()
        if request.form.get('comment_' + str(quest_id)):
            print(2)
            quest.comment = request.form['comment_' + str(quest_id)].strip()
        if request.form.get('select_category_question_edit_redactor_' + str(quest_id)):
            print(3)
            quest.category = session.query(Category).filter(
                Category.name == request.form['select_category_question_edit_redactor_' + str(quest_id)]).first().id
        if request.form.get('answer_' + str(quest_id)) and \
                request.form.get('wrong_answer1_' + str(quest_id)) \
                and request.form.get('wrong_answer2_' + str(quest_id))\
                and request.form.get('wrong_answer3_' + str(quest_id)):
            print(4)
            quest.answers = '!@#$%'.join([request.form['answer_' + str(quest_id)].strip(),
                                          request.form['wrong_answer1_' + str(quest_id)].strip(),
                                          request.form['wrong_answer2_' + str(quest_id)].strip(),
                                          request.form['wrong_answer3_' + str(quest_id)].strip()])
        if request.form.get('answer_' + str(quest_id)):
            print(5)
            quest.right_answer = request.form['answer_' + str(quest_id)].strip()
        if request.form.get('select_type_question_edit_redactor_' + str(quest_id)):
            print(6)
            quest.type = request.form['select_type_question_edit_redactor_' + str(quest_id)]
        if request.form.get('select_comp_question_edit_redactor_' + str(quest_id)):
            print(7)
            quest.complexity = request.form['select_comp_question_edit_redactor_' + str(quest_id)]
        if request.files.get('image_' + str(quest_id)):
            print(8)
            os.remove(quest.images[1:])
            quest.images = f'/static/img/questions/{quest.id}+{get_time()}.png'
            with open(quest.images[1:], 'wb') as f1:  # 10
                f1.write(request.files['image_' + str(quest_id)].read())
        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})