from app import app, db
from app.forms import PersonForm
from flask import render_template, flash, redirect, url_for, request

# Import the models
from app.models import Person

@app.route("/")
def index():
    return redirect(url_for('people'))

@app.route("/people")
def people():
    people = Person.query.all()
    return render_template("all_people.html", people=people)

# Route for adding and editing a Person
@app.route('/person/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    person = Person.query.get(id)
    form = PersonForm(obj=person)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(person)
        db.session.commit()
        return redirect(url_for('view_person', id=id))

    return render_template('person_form.html', form=form, person=person)


# Route for adding and editing a Person
@app.route('/delete/<int:id>', methods=['POST'])
def delete_person(id):
    
    person = Person.query.get(id)
    if person:
        # Delete the Person from the database
        db.session.delete(person)
        db.session.commit()
        return redirect(url_for('people'))

    return redirect(url_for('people'))

# Route for viewing a Person
@app.route('/view/<int:id>', methods=['GET'])
def view_person(id):
    person = Person.query.get(id)
    return render_template('person_view.html', person=person)