# Before runing this file make sure you set DATABASE_URL:
# export DATABASE_URL=postgres://eympoeyrcypiba:30c1fb7fd8e0bedf747d826d1ebc8c40039a0b2a07c3f906ee17faa90c017c37@ec2-107-22-197-30.compute-1.amazonaws.com:5432/d46pko3dnpg4bk

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
from datetime import datetime
from booksite import db
from booksite import login_manager

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # it runs a query on the post table and graps all posts posted by this user

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#
# class Book(db.Model):
#     __tablename__ = "books"
#     isbn = db.Column(db.String, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     author = db.Column(db.String, nullable=False)
#     year = db.Column(db.Integer, nullable=False)
#
# class Review(db.Model):
#     __tablename__ = "reviews"
#     user_id = db.Column(db.Integer, primary_key=True)
#     # book_isbn = db.Column(db.String, nullable=False)
#     comment = db.Column(db.String, nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     book_id = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
#
# class Users(db.Model):
#     __tablename__ = "users"
#     user_id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.String, nullable=False)
#     user_password = db.Column(db.String, nullable=False)
