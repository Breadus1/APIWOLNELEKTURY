from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import AppConfig
import logging

database = SQLAlchemy()

def initialize_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    database.init_app(app)

    with app.app_context():
        from .routes import configure_routes
        configure_routes(app)
        database.create_all()

    logging.basicConfig(level=app.config['LOGGING_LEVEL'])
    app.logger.setLevel(app.config['LOGGING_LEVEL'])

    return app
