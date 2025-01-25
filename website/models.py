from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    # Relationships
    notes = db.relationship('Note', backref='user', lazy=True)
    books = db.relationship('Book', backref='user', lazy=True)


class Note(db.Model):
    __tablename__ = 'note'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)  # Ensure the field is not nullable
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key with not null constraint


class Book(db.Model):
    __tablename__ = 'book'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    poem = db.Column(db.String(5000))  # Poem can be nullable if it's optional
    quote = db.Column(db.String(5000))  # Quote can be nullable if it's optional
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key with not null constraint

