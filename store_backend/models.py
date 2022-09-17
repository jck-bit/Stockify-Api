from store_backend import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    admin = db.Column(db.Boolean)
    sales = db.relationship('Sales', backref='author', lazy=True)

    def __repr__(self) :
        return f"User('{self.name}', '{self.sales}', '{self.public_id}')"

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    total_sales = db.Column(db.Integer)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Sales('{self.name}', '{self.total_sales}','{self.date_sold}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    Quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"Products('{self.name}', '{self.price}','{self.Quantity}')"
