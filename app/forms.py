from app import db
from app.models import Person
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired



class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    parents = StringField('Parents')
    siblings = StringField('Siblings')
    title = TextAreaField('Title')
    bio = TextAreaField('Bio')