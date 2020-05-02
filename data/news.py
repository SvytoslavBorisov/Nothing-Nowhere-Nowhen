import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    caption = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now)