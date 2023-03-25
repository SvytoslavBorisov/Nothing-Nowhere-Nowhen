from flask import Blueprint, jsonify
from app.data.news import News
from app.data import db_session
import os
import configparser

'''Cоздаём объекта парсера. Читаем конфигурационный файл'''
config = configparser.ConfigParser()
config.read("config.ini", encoding='utf-8')

"""Загрузка переменных среды из файла"""
from dotenv import load_dotenv
load_dotenv(dotenv_path=config['PATH']['SECRET_DATA'])


blueprint = Blueprint('news_api', __name__, template_folder='templates')


'''API для удаления вопроса'''
@blueprint.route(f'/api/{ os.getenv("TOKEN") }/news/<int:new_id>', methods=['DELETE'])
def delete_questions(new_id):
    session = db_session.create_session()
    new = session.query(News).get(new_id)
    if not new:
        return jsonify({'error': 'Not found'})
    session.delete(new)
    session.commit()
    return jsonify({'success': 'OK'})