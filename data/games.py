import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))

    result = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    who_play = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    orm_with_category = orm.relation('Category')
    orm_with_users = orm.relation('User')
