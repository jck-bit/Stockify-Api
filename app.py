from flask import Flask, request, jsonify
from products import products

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'welcome to the Api'

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

#get one product
@app.route('/products/<string:name>', methods=['GET'])
def get_product(name):
    for product in products:
        if product['name'] == name:
            return jsonify(product)
    return jsonify({'message': 'product not found'})

#add_product
@app.route('/products', methods=['POST'])
def create_product():
    product = request.get_json()
    products.append(product)
    return jsonify ({'message': 'product added successfully'})

#delete product
@app.route('/products/<string:name>', methods=['DELETE'])
def delete_product(name):
    for product in products:
        if product['name'] == name:
            products.remove(product)
            return jsonify({'message': 'product deleted successfully'})
    return jsonify({'message': 'product not found'})



if __name__ == '__main__':
    app.run(debug=True)