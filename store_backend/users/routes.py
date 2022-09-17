from flask import Blueprint,jsonify, request,make_response
from store_backend import db, app
from store_backend.models import Sales, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
import uuid
from flask_mail import Message
from flask_jwt_extended import create_access_token
from functools import wraps


users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    
    output = []

    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['image_file'] = user.image_file
        user_data['public_id'] = user.public_id
        user_data['password'] = user.password
        user_data['sales'] = user.sales
        user_data['admin'] = user.admin
        
        output.append(user_data)

    return jsonify({"users": output})

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
def create_token():

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username == "":
        msg = "The username field cannot be empty"
        return {"status": "Failed", "message": msg},401
    if password == "":
        msg = "The password field cannot be empty"
        return {"status": "Failed", "message": msg}, 401
    
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return {"status":"Failed","message": "Invalid username or password"}, 401

    login_user(user)
    access_token = create_access_token(identity=username)
    return  {"status":"success","token":access_token}, 200


@users.route('/users', methods=['POST'])
def create_user():
    
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    confirm_password = request.json.get('confirm_password')

    if username =="":
         msg = "The username field cannot be empty"
         return {"status": "Failed", "message": msg},401

    if password == "":
        msg = "The password field cannot be empty"
        return {"status": "Failed", "message": msg}, 401
    
    if confirm_password != password:
        msg = "The two passwords must match"
        return {"status": "Failed", "message": msg}, 401
    
    user = User.query.filter_by(username=username).first()
    
    
    if user:
        msg = "User alraedy exists.Try another username"
        return {"status": "Failed", "message": msg}, 401
    
    new_user = User(public_id=str(uuid.uuid4()), username=username, password=generate_password_hash(password), admin=False)
    db.session.add(new_user)
    db.session.commit()

    msg = "New user created"
    return {"status":"success","message":msg}