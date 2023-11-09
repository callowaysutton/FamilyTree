from app import app, db
from app.forms import EditPerson, AddPerson
from flask import render_template, flash, redirect, url_for, request

# Import the models
from app.models import Person

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/people")
def people():
    people = Person.query.all()
    return render_template("people.html", people=people)

@app.route('/edit/<int:person_id>', methods=['GET', 'POST'])
def edit_person(person_id):
    # Fetch the person object from the database based on the person_id
    person = Person.query.get_or_404(person_id)
    
    # Create an instance of the EditPerson form
    form = EditPerson(person=person)

    if form.validate_on_submit():
        # Update the person's name with the new value
        person.name = form.name.data
        db.session.commit()
        flash('Person information updated successfully', 'success')
        return redirect(url_for('view', person_id=person.id))

    return render_template('editperson.html', form=form, person=person)

@app.route('/view/<int:person_id>', methods=['GET'])
def view(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template("view.html", person=person)

@app.route("/add")
def add():
    return render_template("addperson.html", AddPerson=AddPerson)