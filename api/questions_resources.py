from __future__ import unicode_literals
from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.questions import Question
from api.parsers import parserForQuestion


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
        args = parserForQuestion.parse_args()
        session = db_session.create_session()
        try:
            quest = Question(
                id=args['id'],
                text=args['text'],
                category=args['category'],
                answers=args['answers'],
                right_answer=args['right_answer'],
                who_add=args['who_add'],
                is_promoted=args['is_promoted']
            )
            session.add(quest)
            session.commit()
        except:
            return jsonify({'error': 'Id already exists'})
        return jsonify({'success': 'OK'})