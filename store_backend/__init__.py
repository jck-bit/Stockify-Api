from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager, create_access_token,get_jwt,get_jwt_identity
from flask_cors import CORS
from datetime import timedelta, datetime, timezone
from config import Config
import json
# from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
# migrate = Migrate(app, db)
jwt = JWTManager(app)
db.init_app(app)
CORS(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

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