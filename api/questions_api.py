from flask import Blueprint, jsonify, request
from app.data.questions import Question
from app.data.categories import Category
from app.data import db_session
import os
from app.secondary_functions import get_time
import configparser

'''Cоздаём объекта парсера. Читаем конфигурационный файл'''
config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

"""Загрузка переменных среды из файла"""
from dotenv import load_dotenv
load_dotenv(dotenv_path=config['PATH']['SECRET_DATA'])


blueprint = Blueprint('questions_api', __name__, template_folder='templates')


'''API для получения одного вопроса'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/question/<int:question_id>',  methods=['GET'])
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
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/questions',  methods=['GET'])
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
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/add_quest', methods=['POST'])
def create_questions():
    session = db_session.create_session()
    try:
        quest = session.query(Question).filter(Question.text == request.form['text'], Question.answers == request.form['answer'],).first()  # 7
        if quest:
            return jsonify({'errors': 'Такой вопрос уже есть в базе'})

        quest = Question(
            text=request.form['text'],
            comment=request.form['comment'],
            right_answer=request.form['answer'],
            answers='!@#$%'.join([request.form['answer'].split('!@#$%')[0],
                     request.form['wrong_answer1'],
                     request.form['wrong_answer2'],
                     request.form['wrong_answer3']]),
            who_add=request.form['who_add'],
            category=request.form['category'],
            type=request.form['type'],
            complexity=request.form['complexity'],
            is_promoted=1 if request.form['state_who_add'] == 'admin' else 0)

        session.add(quest)
        session.commit()

        file = request.files['file'].read()
        if str(file) != "b''":
            quest.images = f'/static/img/questions/{quest.id}.png'
            with open(quest.images[1:], 'wb') as f1:  # 10
                f1.write(file)
        else:
            quest.images = ' '

        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'errors': 'Неизвестная ошибка'})

    try:
        session.add(quest)
        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'errors': 'Неизвестная ошибка'})
    return jsonify({'success': 'OK'})


'''API для удаления вопроса'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/quests/<int:quest_id>', methods=['DELETE'])
def delete_questions(quest_id):
    session = db_session.create_session()
    quest = session.query(Question).get(quest_id)
    if not quest:
        return jsonify({'error': 'Not found'})
    session.delete(quest)
    session.commit()
    return jsonify({'success': 'OK'})


'''API для редактирования вопроса'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/quests/<int:quest_id>', methods=['PUT'])
def put_questions(quest_id):
    session = db_session.create_session()
    quest = session.query(Question).get(quest_id)
    if not quest:
        return jsonify({'error': 'Not found'})
    try:
        if request.form.get('text_' + str(quest_id)):
            quest.text = request.form['text_' + str(quest_id)].strip()
        if request.form.get('comment_' + str(quest_id)):
            quest.comment = request.form['comment_' + str(quest_id)].strip()
        if request.form.get('select_category_question_edit_redactor_' + str(quest_id)):
            quest.category = session.query(Category).filter(
                Category.name == request.form['select_category_question_edit_redactor_' + str(quest_id)]).first().id
        if request.form.get('answer_' + str(quest_id)) and \
                request.form.get('wrong_answer1_' + str(quest_id)) \
                and request.form.get('wrong_answer2_' + str(quest_id))\
                and request.form.get('wrong_answer3_' + str(quest_id)):
            quest.answers = '!@#$%'.join([request.form['answer_' + str(quest_id)].strip().split('!@#$%')[0],
                                          request.form['wrong_answer1_' + str(quest_id)].strip(),
                                          request.form['wrong_answer2_' + str(quest_id)].strip(),
                                          request.form['wrong_answer3_' + str(quest_id)].strip()])
        if request.form.get('answer_' + str(quest_id)):
            quest.right_answer = request.form['answer_' + str(quest_id)].strip()
        if request.form.get('select_type_question_edit_redactor_' + str(quest_id)):
            quest.type = request.form['select_type_question_edit_redactor_' + str(quest_id)]
        if request.form.get('select_comp_question_edit_redactor_' + str(quest_id)):
            quest.complexity = request.form['select_comp_question_edit_redactor_' + str(quest_id)]
        if request.files.get('image_' + str(quest_id)):
            file = request.files['image_' + str(quest_id)].read()
            if str(file) != "b''":
                if quest.images[1:]:
                    os.remove(quest.images[1:])
                quest.images = f'/static/img/questions/{quest.id}+{get_time()}.png'
                with open(quest.images[1:], 'wb') as f1:  # 10
                    f1.write(file)
            elif request.form.get('hidden_image_' + str(quest_id)):
                if request.form['hidden_image_' + str(quest_id)] == 'no_image':
                    quest.images = ' '
        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error': 'error type'})
    return jsonify({'success': 'OK'})