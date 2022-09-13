from unicodedata import name
from flask import Blueprint,jsonify, request
from store_backend import db
from store_backend.models import Sales, User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_mail import Message

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "New user created"})

@users.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['name'] = user.name
        user_data['image_file'] = user.image_file
        user_data['public_id'] = user.public_id
        user_data['password'] = user.password
        user_data['sales'] = user.sales

        output.append(user_data)

    return jsonify({"users": output})

@users.route('/users/<public_id>', methods=['GET'])
def get_one_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({"user not found"})

    user_data = {}

    user_data['name'] = user.name
    user_data['public_id'] = user.public_id
    user_data['admin'] = user.admin
    user_data['password'] = user.password
    user_data['image_file'] = user.image_file
    user_data['sales'] = user.sales

    return jsonify({"user": user_data})

@users.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    name = "".join(data['name'].split())
    password = "".join(data['password'].split())

    if name == '':
        msg = 'Username cannot be empty'
        return {"status":"Failed!" ,"message": msg},400
    if password == '':
        msg = 'The password Field cannot be empty'
        return {"status":"Failed!" ,"message": msg},400

    user =User.query.filter_by(name=data['name'])
    if not user or not check_password_hash(user[4], password):
        return {"status":"Failed", "message":"Invalid credentials"}, 400
    
    return {"status":"Success"}

    