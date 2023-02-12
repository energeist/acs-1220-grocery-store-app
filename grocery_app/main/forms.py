from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from grocery_app.models import ItemCategory, GroceryStore, GroceryItem, User
from grocery_app.extensions import app, db, bcrypt
from wtforms.fields.html5 import DateField

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Store Name')
    address = StringField('Address')
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button

    name = StringField('Item Name', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="Your store name needs to be betweeen 3 and 80 chars")
        ])
    price = FloatField('Item Price', validators=[DataRequired()])
    category = SelectField('Category', choices=ItemCategory.choices(), validators=[DataRequired()])
    photo_url = StringField('Photo URL', validators=[DataRequired()])
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query, validators=[DataRequired()])
    submit = SubmitField('Submit')