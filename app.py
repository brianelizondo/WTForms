"""App for Pet Adoption Agency aplication"""

from crypt import methods
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from forms import AddPetForm, EditPetForm
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
    pets_availables = Pet.query.filter_by(available=True).order_by(desc(Pet.id)).all()
    pets_no_availables = Pet.query.filter_by(available=False).order_by(desc(Pet.id)).all()
    return render_template("home.html", pets_availables=pets_availables, pets_no_availables=pets_no_availables)

@app.route("/add", methods=["GET", "POST"])
def show_add_pets_form():
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

@app.route("/<int:pet_id>")
def show_pets_details(pet_id):
    """
    Show information about the given pet
    Have a button to get to edit page
    """
    pet = Pet.query.get_or_404(pet_id)
    return render_template("pets_details.html", pet=pet)

@app.route("/edit/<int:pet_id>", methods=["GET", "POST"])
def show_pets_edit_form(pet_id):
    """
    Show the edit page for a pet
    Have a cancel button that returns to the detail page for a pet, and a save button that updates the pet
    """

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        db.session.commit()
        flash(f"The pet '{pet.name}' was updated!")
        return redirect(f"/{pet_id}")

    else:
        return render_template("pets_edit.html", form=form, pet=pet)