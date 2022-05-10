"""Forms for Pet Adoption Agency aplication"""
from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, URL, NumberRange, Optional

class AddPetForm(FlaskForm):
    """Form for adding Pets"""

    name = StringField("Pet Name", validators=[InputRequired(message='Please enter the Pet Name')])
    species = SelectField("Species", choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine'), ('pork', 'Pork'), ('rabbit', 'Rabbit')])
    photo_url = URLField("Photo URL", validators=[Optional(), URL(message='Please enter a valid URL')])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=100, message='Please enter an Age between 0 - 100')])
    notes = TextAreaField("Notes", validators=[Optional()])
    