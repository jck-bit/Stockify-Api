from flask import Blueprint,jsonify,request
from store_backend import db
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
    description = request.form.get('description', None)
    image_file = request.files.get('product_pic', None)

    #if no product pic, the product will get a default pic from the supabase bucket
    if not image_file:
        image_url = supabase.storage.from_("product_pics").get_public_url("product_default.jpg")
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

    new_product = Product(name=name, price=price, quantity=quantity,description=description, image_file=image_url)
    
    db.session.add(new_product)
    db.session.commit()


    serialized_product = {
        'id': new_product.id,
        'name': new_product.name,
        'price': new_product.price,
        'quantity': new_product.quantity,
        'description': new_product.description,
        'image_file': new_product.image_file
    }
    return jsonify({'message': 'Product added successfully', 'product': serialized_product}), 201


@products.route('/products', methods=['GET'])
@jwt_required()
def get_all_products():
    products = Product.query.all()
    
    return jsonify ({'products':  [{'id':product.id, 
                                    'name':product.name,
                                    'price':product.price,
                                    'date_added':product.date_added,
                                    'quantity':product.quantity,
                                    'product_pic':product.image_file,
                                    'description':product.description
                                    } for product in products]})

@products.route('/products/<name>', methods=['GET'])
def get_one_product(name):
    product = Product.query.filter_by(name=name).first()

    if not product:

        return jsonify({'message': 'No product found'}), 404

    product_data = {}
    product_data['name'] = product.name
    product_data['price'] = product.price
    product_data['quantity'] = product.quantity

    return jsonify(product_data)


@products.route('/products/<id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    name = request.json.get('name')
    price = request.json.get('price')
    quantity = request.json.get('quantity')
    description = request.json.get('description')
    image_file = request.json.get('image')

    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify({'message': 'No product found'}),404

    if not image_file:
        image_url = supabase.storage.from_("product_pics").get_public_url("product_default.jpg")
    else:
        # Upload the new image to the supabase bucket
        filename = secure_filename(image_file['filename'])
        file_data = image_file['data']
        bucket_name = 'product_pics'
        supabase.storage.from_(bucket_name).upload(filename, file_data)

        # Remove the old image and create a new one
        if product.image_file != 'product_default.jpg':
            supabase.storage.from_(bucket_name).remove(product.image_file)

        image_url = supabase.storage.from_(bucket_name).get_public_url(filename)

    product.name = name
    product.price = price
    product.quantity = quantity
    product.description = description
    product.image_file = image_url

    db.session.commit()
    #returning the updated product as json
    product_dict = {"id":product.id,"name":product.name,"price":product.price,"quantity":product.quantity,"description":product.description,"product_pic":product.image_file,"date_added":product.date_added}
    return jsonify({'message': 'Product updated successfully', 'product': product_dict}), 200


@products.route('/products/<id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.filter_by(id=id).first()

    if not product:
        return jsonify({'message': 'Product does not Exist'}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product has been deleted successfully!'}), 200
