# Before runing this file make sure you set DATABASE_URL:
# export DATABASE_URL=postgres://eympoeyrcypiba:30c1fb7fd8e0bedf747d826d1ebc8c40039a0b2a07c3f906ee17faa90c017c37@ec2-107-22-197-30.compute-1.amazonaws.com:5432/d46pko3dnpg4bk

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    user_id = db.Column(db.Integer, primary_key=True)
    # book_isbn = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)

class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    user_password = db.Column(db.String, nullable=False)
