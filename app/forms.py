from app import db
from app.models import Person
import wtforms

class EditPerson():
    def __init__(self, person):
        self.person = person
        self.id = wtforms.StringField("Name", validators=[wtforms.validators.DataRequired()])
        self.submit = wtforms.SubmitField("Submit")

    def validate(self):
        if not wtforms.Form.validate(self):
            return False
        if self.person.name == self.name.data:
            return True
        if db.session.query(Person).filter_by(name=self.name.data).first():
            self.name.errors.append("Name already in use")
            return False
        return True