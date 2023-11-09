from app import app, db
from flask import render_template

# Import the models
from app.models import Person

@app.route("/")
def index():
    return render_template("index.html")