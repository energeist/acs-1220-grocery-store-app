import os
from os.path import exists
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User, shopping_list_table
from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm, CartForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    for store in all_stores:
        print(store.title)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.is_submitted():
        new_grocery_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by=current_user
        )
        db.session.add(new_grocery_store)
        db.session.commit()
        flash('New store was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_grocery_store.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        image_exists = os.path.exists(f'../static/img/{form.photo_url.data}')
        print(f"image exists: {image_exists}")
        print(current_user)
        if image_exists:
            image_url = form.photo_url.data
        else:
            image_url = '/static/img/no_image.jpeg'
        new_grocery_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=image_url,
            store=form.store.data,
            created_by=current_user
        )
        db.session.add(new_grocery_item)
        db.session.commit()
        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_grocery_item.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id) # first query is to get the store data for modification
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        # last_edit_id = current_user
        db.session.commit()
        flash('Store was edited successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id) # second query is to return the most recent (edited) data to the item details page
    return render_template('store_detail.html', form=form, store=store)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        image_exists = os.path.exists(f'/static/img/{form.photo_url.data}')
        print(f"image exists: {image_exists}")
        if image_exists:
            image_url = form.photo_url.data
        else:
            image_url = '/static/img/no_image.jpeg'
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = image_url
        item.store = form.store.data
        # last_edit_id = current_user
        db.session.commit()
        flash('Item was edited successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', form=form, item=item)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    # ... adds item to current_user's shopping list
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)
    db.session.commit()
    print(f"{item.name} added to cart")
    flash(f"{item.name} added to cart")
    return redirect(url_for("main.shopping_list", item_id=item.id))

@main.route('/shopping_list')
@login_required
def shopping_list():
    # ... get logged in user's shopping list items ...
    # ... display shopping list items in a template ...
    shopping_list = current_user.shopping_list_items
    return render_template("shopping_list.html", shopping_list=shopping_list)