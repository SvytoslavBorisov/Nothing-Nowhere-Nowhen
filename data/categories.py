import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    orm_with_game = orm.relation("Game")


'''
    id             - ID
    name           - Название категории
    description    - Описание категории
    image          - Картинка категории
    orm_with_game  - Связь с играми
'''