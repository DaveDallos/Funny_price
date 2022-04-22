import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cart = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # user = orm.relation("Users", back_populates='user')

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self.id} {self.name} {self.email} {self.created_date}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        User(hashed_password=self.hashed_password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
