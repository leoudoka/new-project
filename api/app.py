from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from apifairy import APIFairy

import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
mail = Mail()
apifairy = APIFairy()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # extensions
    from api import models
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    if app.config['USE_CORS']:  # pragma: no branch
        cors.init_app(app)
    mail.init_app(app)
    apifairy.init_app(app)

    # blueprints
    from api.errors import errors
    app.register_blueprint(errors)
    from api.services.auth.routes import tokens
    app.register_blueprint(tokens, url_prefix='/api')
    from api.services.users.routes import users
    app.register_blueprint(users, url_prefix='/api')

    @app.route('/')
    def index():  # pragma: no cover
        return redirect(url_for('apifairy.docs'))

    @app.after_request
    def after_request(response):
        # Werkzeug sometimes does not flush the request body so we do it here
        request.get_data()
        return response

    return app