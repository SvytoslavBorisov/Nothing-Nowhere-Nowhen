from __future__ import unicode_literals
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session, users, questions
from data.categories import Category
from data.questions import Question
from data.users import User
from data.games import Game
import json


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('text', required=True)
parser.add_argument('answers', required=True)
parser.add_argument('category', required=True)
parser.add_argument('right_answer', required=True)
parser.add_argument('is_promoted', required=True, type=bool)
parser.add_argument('who_add', required=True, type=int)


def abort_if_questions_not_found(quest_id):
    session = db_session.create_session()
    if quest_id.isdigit():
        questions = session.query(Question).get(quest_id)
        if not questions:
            abort(404, message=f"Questions {quest_id} not found")
    else:
        abort(404, message=f"Question id is not integer")


class QuestionResource(Resource):
    def get(self, question_id):
        abort_if_questions_not_found(question_id)
        session = db_session.create_session()
        questions = session.query(Question).get(question_id)
        return jsonify(
            {
                'question':
                    questions.to_dict(only=('id', 'text', 'category', 'who_add', 'answers', 'right_answer'))
            }
        )

    def delete(self, questions_id):
        abort_if_questions_not_found(questions_id)
        session = db_session.create_session()
        questions = session.query(Question).get(questions_id)
        session.delete(questions)
        session.commit()
        return jsonify({'success': 'OK'})


class QuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        questions = session.query(Question).all()

        return jsonify(
            {
                'questions':
                    [item.to_dict(only=('id', 'text', 'category.name', 'who_add.name', 'answers', 'right_answer'))
                     for item in questions]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        questions = Question(
            text=args['text'],
            category=args['category'],
            who_add=args['who_add'],
            is_promoted=args['is_promoted']
        )

        session.add(questions)
        session.commit()
        return jsonify({'success': 'OK'})