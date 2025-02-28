from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship

from constants import Age, Category, Gender, Profile

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    has_answered = Column(Boolean, default=False)
    # Relationship
    info = relationship('UserInfo', back_populates='user', uselist=False, passive_deletes=True)
    wines = relationship('Wine', secondary='purchases', back_populates='users', passive_deletes=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
class UserInfo(db.Model):
    __tablename__ = 'users_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, unique=True)
    gender = Column(Enum(Gender), nullable=False)
    age = Column(Enum(Age), nullable=False)
    # Relationships
    user = relationship('User', back_populates='info')
    profiles = relationship('Profile', secondary='user_profiles', back_populates='users_inf', passive_deletes=True)

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(Profile), unique=True, nullable=False)
    # Relationship
    users_inf = relationship('UserInfo', secondary='user_profiles', back_populates='profiles', passive_deletes=True)

user_profile = Table(
    'user_profiles', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users_info.id', ondelete='CASCADE'), primary_key=True),
    Column('profile_id', Integer, ForeignKey('profiles.id', ondelete='CASCADE'), primary_key=True)
)

class Wine(db.Model):
    __tablename__ = 'wines'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(80), nullable=False, index=True, unique=True)
    name = Column(String(200), nullable=False, unique=True)
    category = Column(Enum(Category), nullable=False)
    year = Column(Integer)
    country = Column(String(50), nullable=False)
    region = Column(String(100))
    den_origin = Column(String(100))
    taste = Column(String(100))
    alcohol = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fruity_spicy = Column(Integer)
    young_barrel = Column(Integer)
    light_body = Column(Integer)
    # winery = Column(String(100))
    # vineyard_age = Column(Integer)
    # award = Column(Boolean, nullable=False)
    # link = Column(String(200), nullable=False)
    
    # Relationships
    grapes = relationship('Grape', secondary='wine_grapes', back_populates='wines', passive_deletes=True)
    foods = relationship('Food', secondary='wine_foods', back_populates='wines', passive_deletes=True)
    users = relationship('User', secondary='purchases', back_populates='wines', passive_deletes=True)

class Compras(db.Model):
     __tablename__ = 'Compras'
     wine_id = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
     user_id = Column('wine_id', Integer,ForeignKey('wines.id', ondelete='CASCADE'), primary_key=True)
     o_wine_id = Column('o_user_id', Integer)
     code = Column(String(80), nullable=False)
     o_user_id = Column('o_wine_id', Integer)
     username = Column(String(50), nullable=False)

purchase = Table(
     'purchases', db.Model.metadata,
     Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
     Column('wine_id', Integer, ForeignKey('wines.id', ondelete='CASCADE'), primary_key=True)
)

class Grape(db.Model):
    __tablename__ = 'grapes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    # Relationship
    wines = relationship('Wine', secondary='wine_grapes', back_populates='grapes', passive_deletes=True)

wine_grape = Table(
    'wine_grapes', db.Model.metadata,
    Column('wine_id', Integer, ForeignKey('wines.id', ondelete='CASCADE'), primary_key=True),
    Column('grape_id', Integer, ForeignKey('grapes.id', ondelete='CASCADE'), primary_key=True)
)


class Food(db.Model):
    __tablename__ = 'foods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    # Relationships
    wines = relationship('Wine', secondary='wine_foods', back_populates='foods', passive_deletes=True)

wine_food = Table(
    'wine_foods', db.Model.metadata,
    Column('wine_id', Integer, ForeignKey('wines.id', ondelete='CASCADE'), primary_key=True),
    Column('foods_id', Integer, ForeignKey('foods.id', ondelete='CASCADE'), primary_key=True)
)