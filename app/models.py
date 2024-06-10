from . import database

class Book(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(128), nullable=False)
    epoch_id = database.Column(database.Integer, database.ForeignKey('epoch.id'), nullable=False)
    genre_id = database.Column(database.Integer, database.ForeignKey('genre.id'), nullable=False)
    kind_id = database.Column(database.Integer, database.ForeignKey('kind.id'), nullable=False)
    author_id = database.Column(database.Integer, database.ForeignKey('author.id'), nullable=False)

class Epoch(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), nullable=False)
    books = database.relationship('Book', backref='epoch', lazy=True)

class Genre(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), nullable=False)
    books = database.relationship('Book', backref='genre', lazy=True)

class Kind(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), nullable=False)
    books = database.relationship('Book', backref='kind', lazy=True)

class Author(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(128), nullable=False)
    books = database.relationship('Book', backref='author', lazy=True)
