from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

JWTManager(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return jsonify({"messsage":"welcome to the  store Api"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'page Not Found'}), 404


from store_backend.products.routes import products
from store_backend.users.routes import users
from store_backend.sales.routes import sales

app.register_blueprint(users)
app.register_blueprint(sales)
app.register_blueprint(products)