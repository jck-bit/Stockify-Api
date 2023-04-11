from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
JWTManager(app)
Migrate(app, db)
db.init_app(app)
CORS(app)

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