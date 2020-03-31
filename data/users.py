import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String)

    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    start_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now)

    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link_vk = sqlalchemy.Column(sqlalchemy.String)

    state = sqlalchemy.Column(sqlalchemy.String, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
