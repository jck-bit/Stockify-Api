from flask import Blueprint,jsonify, request
from store_backend.models import Sales

sales = Blueprint('sales', '__name__')

@sales.route('/sales', methods=['GET'])
def get_all_sales():

    sales = Sales.query.all()
    
    return jsonify({'sales': [{'id': sale.id, 'total_sale':sale.total_sales, 'user': sale.user_id, 'date':sale.date_sold, 'product':sale.product_id} for sale in sales]})

@sales.route('/sales/<id>')
def get_sale_by_id(id):

    sale = Sales.query.filter_by(id=id).first()

    return jsonify({'sale':[{'id':sale.id, 'user':sale.user_id, 'product_sold':sale.product_id,'date':sale.date_sold}]})