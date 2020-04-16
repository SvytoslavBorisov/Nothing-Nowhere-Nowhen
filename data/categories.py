import sqlalchemy
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
