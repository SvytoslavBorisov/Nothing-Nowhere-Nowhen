import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)

    category = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))

    answers = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    right_answer = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    who_add = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    images = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    is_promoted = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    complexity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    orm_with_category = orm.relation('Category')
    orm_with_users = orm.relation('User')


'''
    id                   - ID
    category             - Категория вопроса
    text                 - Текст вопроса
    answers              - Варианты ответов
    right_answer         - Правильный вариант
    who_add              - Кто добавил
    is_promoted          - Проверен ли вопрос модератором
    images               - Картинка к вопросу
    comment              - Комментарий к вопросу
    type                 - Тип вопроса (write - вводить ответ, change - выбор из 4, all - оба варианта)
    complexity           - Сложность вопроса (от 1 до 5)
    orm_with_category    - Связь с категорией
    orm_with_users       - Связь с игроком, который добавил
'''