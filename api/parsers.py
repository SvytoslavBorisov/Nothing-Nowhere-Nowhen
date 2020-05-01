from flask_restful import reqparse


parserForUser = reqparse.RequestParser()
parserForUser.add_argument('name', required=True)
parserForUser.add_argument('surname', required=True)
parserForUser.add_argument('nickname', required=True)
parserForUser.add_argument('email', required=True)
parserForUser.add_argument('rating', required=True, type=int)

parserForQuestion = reqparse.RequestParser()
parserForQuestion.add_argument('id', required=True, type=int)
parserForQuestion.add_argument('text', required=True)
parserForQuestion.add_argument('category', required=True, type=int)
parserForQuestion.add_argument('answers', required=True)
parserForQuestion.add_argument('right_answer', required=True)
parserForQuestion.add_argument('who_add', required=True, type=int)
parserForQuestion.add_argument('is_promoted', required=True, type=bool)