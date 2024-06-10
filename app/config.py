import os

class AppConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@database/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_LEVEL = 'DEBUG'
