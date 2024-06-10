from flask import request, jsonify, current_app
from . import database
from .models import Book, Epoch, Genre, Kind, Author
from .services import insert_book, insert_categories, fetch_books

def configure_routes(app):
    @app.route('/')
    def home():
        return "Hello, Universe!"

    @app.route('/books', methods=['POST'])
    def add_book():
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

    @app.route('/categories', methods=['POST'])
    def add_categories():
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

    @app.route('/books', methods=['GET'])
    def get_books():
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

    @app.route('/epochs', methods=['GET'])
    def get_epochs():
        epochs = Epoch.query.all()
        return jsonify([{"id": epoch.id, "name": epoch.name} for epoch in epochs]), 200

    @app.route('/genres', methods=['GET'])
    def get_genres():
        genres = Genre.query.all()
        return jsonify([{"id": genre.id, "name": genre.name} for genre in genres]), 200

    @app.route('/kinds', methods=['GET'])
    def get_kinds():
        kinds = Kind.query.all()
        return jsonify([{"id": kind.id, "name": kind.name} for kind in kinds]), 200

    @app.route('/authors', methods=['GET'])
    def get_authors():
        authors = Author.query.all()
        return jsonify([{"id": author.id, "name": author.name} for author in authors]), 200
