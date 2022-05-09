from crypt import methods
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from models import db, connect_db, Pet

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcd1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 Error Page"""
    return render_template('404.html'), 404

@app.route("/")
def home_page():
    """Homepage """

    pets = Pet.query.order_by(desc(Pet.id)).all()
    return render_template("home.html", pets=pets)