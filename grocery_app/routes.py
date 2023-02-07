import os
from os.path import exists
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

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
        )
        db.session.add(new_grocery_store)
        db.session.commit()
        flash('New store was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_grocery_store.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        image_exists = os.path.exists(f'../static/{form.photo_url.data}')
        print(f"image exists: {image_exists}")
        if image_exists:
            image_url = form.photo_url.data
        else:
            image_url = '/static/img/no_image.jpeg'
        new_grocery_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=image_url,
            store=form.store.data
        )
        db.session.add(new_grocery_item)
        db.session.commit()
        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_grocery_item.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
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
        db.session.commit()
        flash('Store was edited successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    # TODO: Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id) # second query is to return the most recent (edited) data to the item details page
    return render_template('store_detail.html', form=form, store=store)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        image_exists = os.path.exists(f'/static/{form.photo_url.data}')
        print(f"image exists: {image_exists}")
        if image_exists:
            print("doing the thing")
            image_url = form.photo_url.data
        else:
            print("not doing the thing")
            image_url = '/static/img/no_image.jpeg'
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = image_url
        item.store = form.store.data
        db.session.commit()
        flash('Item was edited successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', form=form, item=item)

