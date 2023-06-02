from flask import Blueprint,jsonify, request
from store_backend.models import Sales
from flask_jwt_extended import  jwt_required

sales = Blueprint('sales', '__name__')

@sales.route('/sales', methods=['GET'])
@jwt_required()
def get_all_sales():

    sales = Sales.query.all()
    
    return jsonify({'sales': [{'id': sale.id, 
                               'total_sale':sale.total_sales, 'user': sale.user_id, 
                               'date':sale.date_sold.strftime("%A, %d/%m"), 'product':sale.product_id} for sale in sales]})

@sales.route('/sales/<id>')
@jwt_required()
def get_sale_by_id(id):

    sale = Sales.query.filter_by(id=id).first()

    return jsonify({'sale':[{'id':sale.id, 'user':sale.user_id, 'product_sold':sale.product_id,'date':sale.date_sold}]})

@sales.route('/sales/user/<id>', methods=['GET'])
@jwt_required()
def get_sales_by_user(id):
    sales = Sales.query.filter_by(user_id=id).all()
    
    return jsonify({'sales': [{'id': sale.id, 'total_sale':sale.total_sales, 'user': sale.user_id, 'date':sale.date_sold, 'product':sale.product_id} for sale in sales]})