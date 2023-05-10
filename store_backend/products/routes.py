from flask import Blueprint,jsonify,request
from store_backend import db
from flask_login import login_required
from store_backend.models import Product
from flask_jwt_extended import  jwt_required
from datetime import datetime
from supabase  import create_client
import os
from werkzeug.utils import secure_filename


url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

supabase =  create_client(url, key)



products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
@jwt_required()
def post_product():

    name = request.form.get('name', None)
    price = request.form.get('price', None)
    quantity = request.form.get('quantity', None)

    image_file = request.files.get('product_pic', None)

    #if no product pic, the product will get a default pic from the supabase bucket
    if not image_file:
        image_file = supabase.storage.from_("product_pics").get_public_url("product_default.jpg")
    else:
        filename = secure_filename(image_file.filename)
        file_data = image_file.read()
        bucket_name = 'product_pics'
        supabase.storage.from_(bucket_name).upload(filename, file_data)

        # remove the old image and create a new one
        product = Product.query.filter_by(name=name).first()
        if product and product.image_file != 'product_default.jpg':
            supabase.storage.from_(bucket_name).remove(product.image_file)

        image_url = supabase.storage.from_(bucket_name).get_public_url(filename)

    new_product = Product(name=name, price=price, quantity=quantity, image_file=image_url)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'})


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
