from flask_sqlalchemy import SQLAlchemy
import flask
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = flask.Flask(__name__)

app.config.from_object("config")
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["UPLOAD_FOLDER"] = "app/static/uploads"

db = SQLAlchemy(app)

from app import routes