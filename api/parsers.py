from flask_restful import reqparse


parserForUser = reqparse.RequestParser()
parserForUser.add_argument('id', required=True, type=int)
parserForUser.add_argument('name', required=True)
parserForUser.add_argument('surname', required=True)
parserForUser.add_argument('nickname', required=True)
parserForUser.add_argument('email', required=True)
parserForUser.add_argument('rating', required=True, type=int)