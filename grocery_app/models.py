from sqlalchemy_utils import URLType
from grocery_app.extensions import db
from grocery_app.utils import FormEnum
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class ItemCategory(FormEnum):
    """Categories of grocery items."""
    PRODUCE = 'Produce'
    DELI = 'Deli'
    BAKERY = 'Bakery'
    PANTRY = 'Pantry'
    FROZEN = 'Frozen'
    OTHER = 'Other'

class GroceryStore(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GroceryItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # last_edit_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'{self.title}'

class GroceryItem(db.Model):
    """Grocery Item model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemCategory), default=ItemCategory.OTHER)
    photo_url = db.Column(URLType)
    store_id = db.Column(db.Integer, db.ForeignKey('grocery_store.id'), nullable=False)
    store = db.relationship('GroceryStore', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # last_edit_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    user_item_lists = db.relationship('User', 
        secondary='user_shopping_list', back_populates='shopping_list_items'
    )

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'{self.name}'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    shopping_list_items = db.relationship('GroceryItem',
        secondary='user_shopping_list', back_populates='user_item_lists'
    )

    def __repr__(self):
        return f'<User: {self.username}>'

shopping_list_table = db.Table('user_shopping_list',
    db.Column('item_id', db.Integer, db.ForeignKey('grocery_item.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# user_stores_table = db.Table('user_stores',
#     db.Column('store_id', db.Integer, db.ForeignKey('store.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )

# user_items_table = db.Table('user_items',
#     db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )