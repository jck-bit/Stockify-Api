from flask import Flask, request, jsonify
from products import products

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return 'welcome to the Api'

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)