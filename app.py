from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from products import products
from sales import sales

app = Flask(__name__)

auth = HTTPBasicAuth()


USER_DATA = {
    
    "admin": "thisispassword",
}

@auth.verify_password
def verify_password(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the API'})   

@app.route('/products', methods=['GET'])
@auth.login_required
def get_products():
    return jsonify(products)

#get one product
@app.route('/products/<string:name>', methods=['GET'])
@auth.login_required
def get_product(name):
    for product in products:
        if product['name'] == name:
            return jsonify(product)
    return jsonify({'message': 'product not found'})

#add_product
@app.route('/products', methods=['POST'])
@auth.login_required
def create_product():
    product = request.get_json()
    products.append(product)
    return jsonify ({'message': 'product added successfully'})

#delete product
@app.route('/products/<string:name>', methods=['DELETE'])
@auth.login_required
def delete_product(name):
    for product in products:
        if product['name'] == name:
            products.remove(product)
            return jsonify({'message': 'product deleted successfully'})
    return jsonify({'message': 'product not found'})

@app.route('/sales', methods=['GET'])
@auth.login_required
def get_sales():
    return jsonify(sales)

@app.route('/sales/<string:name>', methods=['GET'])
@auth.login_required
def get_sale(name):
    for sale in sales:
        if sale['name'] == name:
            return jsonify(sale)
    return jsonify({'message': 'sale not found'})


if __name__ == '__main__':
    app.run(host = "localhost", port =8000,debug=True)
