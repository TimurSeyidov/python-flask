import sqlalchemy
from sqlalchemy import orm
from datetime import datetime as dt
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__: str = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    about = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True
    )
    email = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
        unique=True,
        nullable=False
    )
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False
    )
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=dt.now
    )
    news = orm.relationship("News", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
