import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True)

    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    start_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now)

    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link_vk = sqlalchemy.Column(sqlalchemy.String)

    state = sqlalchemy.Column(sqlalchemy.String, unique=True)

    wins = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    defeats = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    all_games = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    add_questions = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    agree_newsletter = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    games = orm.relation("Game", back_populates='orm_with_users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_procent_win(self):
        if self.all_games:
            return int((self.wins / self.all_games) * 100)
        return 50


'''
    id                 - ID
    surname            - Фамилия
    name               - Имя
    nickname           - Никнейм
    email              - Почта
    password           - Пароль
    rating             - Рейтинг
    start_date         - Дата регистрации
    avatar             - Аватарка
    link_vk            - Ссылка на VK
    state              - Статус пользователя (admin, user)
    wins               - Кол-во побед
    defeats            - Кол-вл поражений
    all_games          - Всего игр
    add_questions      - Количество добавленных вопросов
    agree_newsletter   - Согласие на рассылку новостей
    games              - Связь с таблицей Games
    set_password()     - Установить пароль
    check_password()   - Проверить пароль 
    get_procent_win()  - Вернуть проценты побед/поражений
'''
