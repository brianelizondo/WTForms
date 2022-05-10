"""Models Pet Adoption Agency aplication"""

from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_PET_PHOTO_PROFILE = "https://cdn3.iconfinder.com/data/icons/avatars-9/145/Avatar_Dog-512.png"

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Create a Pet model for a pet potentially available for adoption"""

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, nullable=False, default=DEFAULT_PET_PHOTO_PROFILE)
    age = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)






