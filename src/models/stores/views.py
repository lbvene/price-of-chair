from flask import Blueprint, render_template, request, redirect, url_for
from models.stores.store import Store
import models.users.decorators as user_decorators

import json

__author__ = 'lbvene'

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    stores = Store.get_all()
    return render_template('stores/store_index.html.j2', stores=stores)

@store_blueprint.route('/<string:store_id>')
@user_decorators.requires_login
def store_page(store_id):
    store = Store.get_by_id(store_id)
    return render_template('stores/store.html.j2', store=store)

@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        # converts string into json
        query = json.loads(request.form['query'])

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html.j2', store=store)

@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.delete_store_success'))

@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def new_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        # converts string into json
        query = json.loads(request.form['query'])

        store = Store(name, url_prefix, tag_name, query)
        store.save_to_mongo()

        return redirect(url_for('.new_store_success'))

    return render_template('stores/new_store.html.j2')

@store_blueprint.route('/new_store_success')
def new_store_success():
    return render_template('stores/new_store_success.html.j2')

@store_blueprint.route('/delete_store_success')
def delete_store_success():
    return render_template('stores/delete_store_success.html.j2')
