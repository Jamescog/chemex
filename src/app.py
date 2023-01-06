from flask import Flask
from flask_cors import CORS
from os import environ
from flask_jwt_extended import JWTManager
from datetime import timedelta

# import blueprint modules
from .auth import auth
from .create_post import createPost
from .render_post import renderPost
from .handle_posts import userActions
from .database import db


def create_app(test_config=None):
    """
    Configuration for application.
    """

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    if test_config is None:
        app.config.from_mapping(
            dbUsername="",
            dbPassword="",
            dbname="",
            SECRET_KEY=environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=1),
            JWT_SECRET_KEY=environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    JWTManager(app)
    db.init_app(app)
    app.url_map.strict_slashes = False
    app.register_blueprint(auth)
    app.register_blueprint(createPost)
    app.register_blueprint(renderPost)
    app.register_blueprint(userActions)
    return app
