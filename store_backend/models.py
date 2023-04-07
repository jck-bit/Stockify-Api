from store_backend import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    admin = db.Column(db.Boolean)
    sales = db.relationship('Sales', backref='user', lazy='dynamic',
                        primaryjoin="User.id == Sales.user_id")
    def __repr__ (self) :
        return f"User('{self.name}', '{self.sales}', '{self.public_id}')"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def  check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_sales = db.Column(db.Integer)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Sales('{self.total_sales}','{self.date_sold}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}','{self.quantity}')"
