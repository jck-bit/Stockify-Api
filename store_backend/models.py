from store_backend import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    admin = db.Column(db.Boolean)
    sales = db.relationship('Sales', backref='user', lazy='dynamic',
                        primaryjoin="User.id == Sales.user_id")

    def __repr__ (self) :
        return f"User('{self.name}', '{self.sales}', '{self.public_id}')"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def  check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_sales = db.Column(db.Integer)
    date_sold = db.Column(db.DateTime, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Sales('{self.total_sales}','{self.date_sold}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}','{self.quantity}')"
