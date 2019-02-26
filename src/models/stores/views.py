from flask import Blueprint, render_template, request, redirect, url_for, json
from src.models.stores.store import Store
import src.common.decorators as decorators

base_model = 'stores'
store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
@decorators.requires_login
def index():
    stores = Store.get_all_store_obj_from_db()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/show/<string:store_id>')
@decorators.requires_login
def show_store(store_id):
    store = Store.get_obj_from_db_by_id(store_id)
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/create', methods=['GET', 'POST'])
@decorators.admin_only
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        #  json.loads converts JSON string to Python dictionary

        store = Store(name, url_prefix, tag_name, query)
        store.save_to_db()
        return redirect(url_for('stores.index'))
    else:
        #  it's a GET not a POST
        return render_template(base_model + '/' + 'create_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@decorators.admin_only
def edit_store(store_id):
    store = Store.get_obj_from_db_by_id(store_id)

    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query = json.loads(request.form['query'])

        store.update_to_db()
        return redirect(url_for('stores.index'))
    else:
        # it's a GET not a POST
        return render_template(base_model + '/' + 'edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@decorators.admin_only
def delete_store(store_id):
    Store.del_from_db_by_id(store_id)
    return redirect(url_for('stores.index'))
