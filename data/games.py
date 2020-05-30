import sqlalchemy
from sqlalchemy import orm
import datetime
from .db_session import SqlAlchemyBase
from secondary_functions import format_date


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))

    result = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    who_play = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    when_play = sqlalchemy.Column(sqlalchemy.Date, default=datetime.date.today(), nullable=True)

    questions = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    result_questions = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    orm_with_users = orm.relation('User')
    orm_with_category = orm.relation('Category', back_populates='orm_with_game')

    def get_date(self):
        return format_date(self.when_play)


'''
    id                   - ID
    category             - Категория игры
    result               - Итог игры
    who_play             - Кто играл
    when_play            - Время игры
    questions            - Вопросы в течение игры
    result_questions     - Результаты ответов на каждый вопрос
    orm_with_users       - Связь с игроком
    orm_with_category    - Связь с категорией
    get_date()           - Вернуть дату в человеческом формате
'''