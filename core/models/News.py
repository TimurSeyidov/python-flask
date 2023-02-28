import sqlalchemy
from sqlalchemy import orm
from datetime import datetime as dt
from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__: str = 'news'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )
    content = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=dt.now
    )
    is_private = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id")
    )
    user = orm.relationship('User')
    categories = orm.relationship("Category",
                          secondary="association",
                          backref="news")
