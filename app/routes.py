from flask import request, jsonify, current_app, render_template
from flask.views import View
from . import database
from .models import Book, Epoch, Genre, Kind, Author
from .services import insert_book, insert_categories, fetch_books

def configure_routes(app):
    app.add_url_rule('/', view_func=HomePage.as_view('home'))
    app.add_url_rule('/books', view_func=AddBook.as_view('add_book'), methods=['POST'])
    app.add_url_rule('/categories', view_func=AddCategories.as_view('add_categories'), methods=['POST'])
    app.add_url_rule('/books', view_func=GetBooks.as_view('get_books'), methods=['GET'])
    app.add_url_rule('/epochs', view_func=GetEpochs.as_view('get_epochs'), methods=['GET'])
    app.add_url_rule('/genres', view_func=GetGenres.as_view('get_genres'), methods=['GET'])
    app.add_url_rule('/kinds', view_func=GetKinds.as_view('get_kinds'), methods=['GET'])
    app.add_url_rule('/authors', view_func=GetAuthors.as_view('get_authors'), methods=['GET'])

class HomePage(View):
    def dispatch_request(self):
        return "Hello, Universe!"

class AddBook(View):
    def dispatch_request(self):
        data = request.json
        current_app.logger.info('Received data: %s', data)
        if not data:
            current_app.logger.error('No input data provided')
            return jsonify({"error": "No input data provided"}), 400

        required_keys = ['title', 'epoch_id', 'genre_id', 'kind_id', 'author_id']
        for key in required_keys:
            if key not in data:
                current_app.logger.error('Missing key: %s', key)
                return jsonify({"error": f"Missing key: {key}"}), 400

        try:
            book = insert_book(data)
            current_app.logger.info('Book created: %s', book)
            return jsonify(book), 201
        except Exception as e:
            current_app.logger.error('Error creating book: %s', e)
            return jsonify({"error": "Internal Server Error"}), 500

class AddCategories(View):
    def dispatch_request(self):
        data = request.json
        current_app.logger.info('Received data: %s', data)
        if not data:
            current_app.logger.error('No input data provided')
            return jsonify({"error": "No input data provided"}), 400

        try:
            categories = insert_categories(data)
            current_app.logger.info('Categories created: %s', categories)
            return jsonify(categories), 201
        except Exception as e:
            current_app.logger.error('Error creating categories: %s', e)
            return jsonify({"error": "Internal Server Error"}), 500

class GetBooks(View):
    def dispatch_request(self):
        filters = request.args
        current_app.logger.info('Received filters: %s', filters)
        try:
            books = fetch_books(filters)
            book_list = []
            for book in books:
                book_data = {
                    'id': book.id,
                    'title': book.title,
                    'epoch': book.epoch.name,
                    'genre': book.genre.name,
                    'kind': book.kind.name,
                    'author': book.author.name
                }
                book_list.append(book_data)
            return jsonify(book_list), 200
        except Exception as e:
            current_app.logger.error('Error getting books: %s', e)
            return jsonify({"error": "Internal Server Error"}), 500

class GetEpochs(View):
    def dispatch_request(self):
        epochs = Epoch.query.all()
        return jsonify([{"id": epoch.id, "name": epoch.name} for epoch in epochs]), 200

class GetGenres(View):
    def dispatch_request(self):
        genres = Genre.query.all()
        return jsonify([{"id": genre.id, "name": genre.name} for genre in genres]), 200

class GetKinds(View):
    def dispatch_request(self):
        kinds = Kind.query.all()
        return jsonify([{"id": kind.id, "name": kind.name} for kind in kinds]), 200

class GetAuthors(View):
    def dispatch_request(self):
        authors = Author.query.all()
        return jsonify([{"id": author.id, "name": author.name} for author in authors]), 200
