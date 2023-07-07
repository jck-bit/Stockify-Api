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

    # create an instance of the Product class
    product = Product()

    # if there is an image file, save it
    if image_file:
        file_data = image_file.read()
        product.save_image(image_file.filename, file_data)

    # set the product attributes
    product.name = name
    product.price = price
    product.quantity = quantity
    product.description = description


    # add the product to the database
    db.session.add(product)
    db.session.commit()

    serialized_product = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'date_added': product.date_added,
        'quantity': product.quantity,
        'product_pic': product.image_file,
        'description': product.description
    }

    return jsonify({
        'message': 'Product created successfully',
        'product': serialized_product
    })


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

    if image_file:
        file_data = image_file.read()
        if secure_filename(image_file.filename):
            #remove the old image
            if product.image_image_file:
                supabase.storage.from_('product_pics').remove(product.image_file)
            
            product.save_image(image_file.filename, file_data)
        
        else:
            return jsonify({'message': 'Invalid file type'}), 400
    
    else:
        product.image_file = product.image_file


    product.name = name
    product.price = price
    product.quantity = quantity
    product.description = description
    

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
