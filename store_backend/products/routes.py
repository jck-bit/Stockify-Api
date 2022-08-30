from flask import Blueprint,jsonify,request
from store_backend import db
from store_backend.models import Product


products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
def post_product():
    data = request.get_json()

    new_product = Product(name=data['name'], price=data['price'], Quantity=data['Quantity'])

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'New product Added!'})

@products.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()

    output = []

    for product in products:
        
        product_data = {}
        product_data['name'] = product.name
        product_data['price'] = product.price
        product_data['Quantity'] = product.Quantity
        output.append(product_data)

    return jsonify({'products': output})

@products.route('/products/<name>', methods=['GET'])
def get_one_product(name):
    product = Product.query.filter_by(name=name).first()

    if not product:
        return jsonify({'message': 'No product found'})

    product_data = {}
    product_data['name'] = product.name
    product_data['price'] = product.price
    product_data['Quantity'] = product.Quantity

    return jsonify(product_data)

@products.route('/products/<name>', methods=['PUT'])
def update_product(name):
    data = request.get_json()

    product = Product.query.filter_by(name=name).first()

    if not product:
        return jsonify({'message': 'No product found'})

    product.name = data['name']
    product.price = data['price']
    product.Quantity = data['Quantity']

    db.session.commit()

    return jsonify({'message': 'Product has been updated!'})


@products.route('/products/<name>', methods=['DELETE'])
def delete_product(name):
    product = Product.query.filter_by(name=name).first()

    if not product:
        return jsonify({'message': 'No product found'})

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product has been deleted!'})