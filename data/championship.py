import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Championship(SqlAlchemyBase):
    __tablename__ = 'championships'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    games = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    procent = sqlalchemy.Column(sqlalchemy.String, nullable=True)