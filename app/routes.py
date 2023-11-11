from app import app, db
from app.forms import PersonForm
import os
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, url_for, request
from flask import Flask, render_template, redirect, url_for
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, WheelZoomTool, ResetTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, show, from_networkx
from bokeh.io import output_file, save
from bokeh.models import HoverTool
from bokeh.embed import components
import pydot
import networkx as nx
import networkx as nx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the models
from app.models import Person

def create_family_tree_graph():
    # Create an empty directed graph
    graph = nx.DiGraph()

    # Query all persons from the database
    persons = Person.query.all()

    # Create a dictionary to store the positions of nodes in each level
    level_positions = {}

    # Function to recursively add nodes and edges
    def add_person_to_graph(person, level):
        if level not in level_positions:
            level_positions[level] = 0

        x = level_positions[level]
        y = -level  # Negative level for vertical spacing

        # Add the person to the graph
        graph.add_node(person.id, name=person.name, x=x, y=y)

        # Increment the position for the next person in the same level
        level_positions[level] += 1

        parents = person.get_parents()
        for parent in parents:
            # Add edges to parents
            graph.add_edge(parent.id, person.id)

            # Recursively add the parent and their siblings
            add_person_to_graph(parent, level + 1)

    # Start building the graph with the root nodes (persons without parents)
    root_nodes = [person for person in persons if not person.get_parents()]
    for root_node in root_nodes:
        add_person_to_graph(root_node, level=0)

    return graph


def create_bokeh_plot(graph):
    # Create a Bokeh plot
    plot = Plot(width=800, height=600,
                x_range=Range1d(-1, 1), y_range=Range1d(-1, 1))

    plot.title.text = "Family Tree Visualization"

    # Create a renderer for the graph
    graph_renderer = from_networkx(graph, nx.spring_layout,
                                    scale=1, center=(0, 0))
    graph_renderer.node_renderer.data_source.data['x'] = [graph.nodes[node]['x'] for node in graph.nodes]
    graph_renderer.node_renderer.data_source.data['y'] = [graph.nodes[node]['y'] for node in graph.nodes]
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="gray", line_alpha=0.8, line_width=1)

    plot.renderers.append(graph_renderer)

    # Add interactive tools
    hover = HoverTool(tooltips=[("Name", "@name")])
    plot.add_tools(hover, TapTool(), BoxSelectTool(), WheelZoomTool(), ResetTool())

    return plot

@app.route("/")
def index():
    # Create a graph using networkx
    graph = create_family_tree_graph()

    # Create a Bokeh plot
    plot = create_bokeh_plot(graph)

    # Generate JavaScript and HTML components for embedding in the web page
    script, div = components(plot)
    return render_template("render_tree.html", script=script, div=div)

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

# Add a new Person
@app.route('/add', methods=['GET', 'POST'])
def add_person():
    form = PersonForm()

    if request.method == 'POST' and form.validate_on_submit():
        person = Person()
        form.populate_obj(person)
        db.session.add(person)        
        db.session.commit()
        id = person.get_id()
        return redirect(url_for('view_person', id=id))

    return render_template('add_person.html', form=form)

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