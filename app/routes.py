from app import app, db
from app.forms import PersonForm
import os
from werkzeug.utils import secure_filename
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

@app.route('/upload', methods=['GET', 'POST'])
def upload_tsv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.tsv'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            with open(file_path, "r") as f:
                for line in f:
                    for name in line.split("\t"):
                        name = name.rstrip()
                        name = name.strip()
                        if name.strip() == "":
                            continue
                        if name:
                            db.session.add(Person(name=name))
            db.session.commit()
            os.remove(file_path)

            return redirect(url_for('index'))  # Redirect to the index page or any other page after successful upload

    return render_template('upload.html')