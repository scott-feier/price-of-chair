from flask import Blueprint

item_blueprint = Blueprint('items', __name__)


@item_blueprint.route('/item/<string:name>')
def item_page():
    pass

#  <span id="priceblock_ourprice" class="a-size-medium a-color-price">$629.00</span>

