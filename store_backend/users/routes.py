from flask import Blueprint,jsonify, request
from store_backend import db, app
from store_backend.models import Sales, User,Product
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required
import uuid
from flask_jwt_extended import create_access_token
import datetime

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_all_users():

    users = User.query.all()

    if not users:
        return jsonify({'users': []})
    
    user_list = []
    for user in users:
        sales_list = []
        for sale in user.sales.all():
            sales_list.append({'id': sale.id, 'total_sales': sale.total_sales, 'date_sold': sale.date_sold})
        user_dict = {'id': user.id, 'username': user.username, 'sales': sales_list}
        user_list.append(user_dict)
    
    return jsonify({'users': user_list})
@users.route('/users/<public_id>', methods=['GET'])
def get_one_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"user not found"})

    user_data = {}

    user_data['username'] = user.username
    user_data['public_id'] = user.public_id
    user_data['admin'] = user.admin
    user_data['password'] = user.password
    user_data['image_file'] = user.image_file
    user_data['sales'] = user.sales

    return jsonify({"user": user_data})

@users.route('/users/<public_id>', methods=['PUT'])
def promote_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"message": "user not found"})

    user.admin = True
    db.session.commit()
    
    return jsonify({"message": "user has been promoted"})

@users.route('/login', methods=["POST"])
def auth_user():

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.get_user_by_email(email=email)

    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=email)
    login_user(user)
    user_dict = {'id': user.id, 'username': user.username, 'public_id': user.public_id, 'email':user.email}
    return ({'message': 'Login successful', 'accessToken':access_token, 'user': user_dict}), 200
        

@app.route('/api/register', methods=['POST'])
def register():

    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.get_user_by_email(email=email)

    if user:
        return jsonify({"message":"user with that email alredy exists"})
    hashed_password = generate_password_hash(password=password)
    new_user = User(public_id=str(uuid.uuid4()), username=username, email=email, password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully!'}), 201

@users.route('/users/sales', methods=['POST'])
def create_sale():
    product_ids = request.json.get('product_ids')
    user_id = request.json.get('user_id')
    quantities = request.json.get('quantities')

    if not product_ids or not user_id or not quantities:
        return jsonify({'error': 'Invalid request body'}),400

    for i in range(len(product_ids)):
        product = Product.query.get(product_ids[i])
        
        if product is None:
            return jsonify({'error': f'Product with id {product_ids[i]} not found'}),400

        if quantities[i] is None:
            return jsonify({'error': f'Quantity not specified for product with id {product_ids[i]}'}),400
        
        if int(quantities[i]) > int(product.quantity):
            return jsonify({'error': f'Requested quantity for product with id {product_ids[i]} is not available'}),400

        total_sales = float(product.price) * int(quantities[i])
        product.quantity -= int(quantities[i])
        date_sold = datetime.datetime.now()
        sale = Sales(product_id=product_ids[i], user_id=user_id, date_sold=date_sold, total_sales=total_sales)
        db.session.add(sale)

    db.session.commit()

    return jsonify({'message':'sale created successfully'}),200


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logout successfull"})