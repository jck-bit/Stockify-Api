from flask import Blueprint,jsonify,request
from store_backend import db
from flask_login import login_required
from store_backend.models import Product
from flask_jwt_extended import  jwt_required

products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
@jwt_required()
def post_product():
    data = request.get_json()

    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'New product Added!'})

@products.route('/products', methods=['GET'])
@jwt_required()
def get_all_products():
    products = Product.query.all()
    
    return jsonify ({'products':  [{'id':product.id, 
                                    'name':product.name,
                                    'price':product.price,
                                    'date_added':product.date_added,
                                    'quantity':product.quantity,
                                    'product_pic':product.image_file
                                    } for product in products]})

@products.route('/products/<name>', methods=['GET'])
def get_one_product(name):
    product = Product.query.filter_by(name=name).first()

    if not product:

        return jsonify({'message': 'No product found'})

    product_data = {}
    product_data['name'] = product.name
    product_data['price'] = product.price
    product_data['quantity'] = product.quantity

    return jsonify(product_data)

@products.route('/products/<name>', methods=['PUT'])
@jwt_required()
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
