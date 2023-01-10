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

app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://database.db"
db.app = app
JWTManager(app)
db.init_app(app)
app.url_map.strict_slashes = False
app.register_blueprint(auth)
app.register_blueprint(createPost)
app.register_blueprint(renderPost)
app.register_blueprint(userActions)

if __name__ == "__main__":
    app.run()
