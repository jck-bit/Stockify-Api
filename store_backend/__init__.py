from flask import Flask
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


from store_backend.products.routes import products
from store_backend.users.routes import users

app.register_blueprint(users)
app.register_blueprint(products)