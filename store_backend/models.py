from store_backend import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from dotenv import  load_dotenv
load_dotenv()
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from  supabase import create_client
import uuid
import os

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

supabase =  create_client(url, key)

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
    image_file = db.Column(db.String(), nullable=False, default='default.jpeg')
    sales = db.relationship('Sales', backref='user', lazy='dynamic',
                        primaryjoin="User.id == Sales.user_id")
      

    def __init__(self, **kwargs):
       super(User, self).__init__(**kwargs)
       self.image_file = supabase.storage.from_("profile_pics").get_public_url("default.jpeg")


    def __repr__(self):
        return f"User('{self.username}', '{self.sales}', '{self.public_id}')"

    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def  check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    
    def save_image(self, filename, file_data):
        bucket_name = 'profile_pics'
        supabase.storage.from_(bucket_name).upload(filename, file_data)

        #remove the old image and create a new one
        if self.image_file != 'default.jpeg':
            supabase.storage.from_(bucket_name).remove(self.image_file)
        
        image_url = supabase.storage.from_(bucket_name).get_public_url(filename)
        self.image_file = image_url
        db.session.commit()

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
    image_file = db.Column(db.String(), nullable=False, default='product_default.jpg')

    # def __init__(self, **kwargs):
    #    super(Product, self).__init__(**kwargs)
    #    self.image_file = supabase.storage.from_("product_pics").get_public_url("product_default.jpg")

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}','{self.quantity}')"

    
    def save_image(self, filename, file_data):
        bucket_name = 'product_pics'
        supabase.storage.from_(bucket_name).upload(filename, file_data)

        #remove the old image and create a new one
        if self.image_file != 'product_default.jpg':
            supabase.storage.from_(bucket_name).remove(self.image_file)
        
        image_url = supabase.storage.from_(bucket_name).get_public_url(filename)
        self.image_file = image_url
        db.session.commit()
        