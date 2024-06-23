import os
from abc import ABCMeta
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


def as_bool(value):
    if value:
        return value.lower() in ['true', 'yes', 'on', '1']
    return False

class IConfig(metaclass=ABCMeta):
    # security options
    ACCESS_TOKEN_MINUTES = int(os.environ.get('ACCESS_TOKEN_MINUTES') or '60')
    REFRESH_TOKEN_DAYS = int(os.environ.get('REFRESH_TOKEN_DAYS') or '7')
    REFRESH_TOKEN_IN_COOKIE = as_bool(os.environ.get(
        'REFRESH_TOKEN_IN_COOKIE') or 'yes')
    REFRESH_TOKEN_IN_BODY = as_bool(os.environ.get('REFRESH_TOKEN_IN_BODY'))
    RESET_TOKEN_MINUTES = int(os.environ.get('RESET_TOKEN_MINUTES') or '15')
    PASSWORD_RESET_URL = os.environ.get('PASSWORD_RESET_URL') or \
        'http://localhost:3000/reset'
    USE_CORS = as_bool(os.environ.get('USE_CORS') or 'yes')
    CORS_SUPPORTS_CREDENTIALS = True

    # API documentation
    APIFAIRY_TITLE = 'Smarthub API'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')
    APIFAIRY_TAGS = ['tokens', 'users']

    # email options
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or '25')
    MAIL_USE_TLS = as_bool(os.environ.get('MAIL_USE_TLS'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER',
                                       'donotreply@smarthub.co')


class DevelopmentConfig(IConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DISABLE_AUTH = as_bool(os.environ.get('DISABLE_AUTH'))
    OAUTH2_PROVIDERS = {}
    OAUTH2_REDIRECT_URI = os.environ.get('OAUTH2_REDIRECT_URI') or \
        'http://localhost:3000/oauth2/{provider}/callback'


class ProductionConfig(IConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    SECRET_KEY = os.environ.get('SECRET_KEY', 'top-secret!')
    DISABLE_AUTH = as_bool(os.environ.get('DISABLE_AUTH'))
    OAUTH2_PROVIDERS = {}
    OAUTH2_REDIRECT_URI = os.environ.get('OAUTH2_REDIRECT_URI') or \
        'http://localhost:3000/oauth2/{provider}/callback'

    