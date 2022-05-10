"""App for Pet Adoption Agency aplication"""

from crypt import methods
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from forms import AddPetForm
from models import db, connect_db, Pet

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcd1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 Error Page
    """
    return render_template('404.html'), 404

@app.route("/")
def home_page():
    """
    Homepage list the pets with name, show photo (if present) and 
    display "Available"if the pet is available for adoption
    """
    pets = Pet.query.order_by(desc(Pet.id)).all()
    return render_template("home.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pets_form():
    """
    Show an add form for pets
    """
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        
        flash(f"The pet '{name}' was added")
        return redirect("/")
    else:
        return render_template("pets_add.html", form=form)