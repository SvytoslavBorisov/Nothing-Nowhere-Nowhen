import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))

    result = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    who_play = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    questions = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    result_questions = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    orm_with_category = orm.relation('Category')
    orm_with_users = orm.relation('User')
