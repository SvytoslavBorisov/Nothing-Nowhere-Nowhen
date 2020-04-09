import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))

    answers = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    right_answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    who_add = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    is_promoted = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    orm_with_category = orm.relation('Category')
    orm_with_users = orm.relation('User')