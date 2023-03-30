# Stockify Store Management is a Shopping API 🛒
 This is a backend for the store-manager. its has been written in pyhton using flask it allows users to interact with a virtual store, where they can view products and make purchases.


## 🚀 Getting Started

To get started, clone this repository and install the dependencies:

run
```
git clone https://github.com/jck-bit/store-manager-backend.git
```
install requirements

```
pip install -r requirements.txt
```
Then, set up the database by running:

```
python3 main.py
```

## 🔑 Authentication

To use the API, you need to create an account and authenticate yourself. You can create an account by sending a POST request to `/users` with your username and password in the body of the request. You can then authenticate yourself by sending a POST request to `/users/auth` with your username and password in the body of the request. The API will return a JWT token that you can use to authenticate future requests.

## 🎯 Features

- View all available products
- View details of a specific product
- Create a new product
- Edit details of a product
- Delete a product
- Create a new sale and update product stock
- View all sales
- View details of a specific sale
- View all users
- Create a new user
- Edit user details
- Delete a user
- Custom error handling for invalid requests


## 🛒 Managing Products
You can manage the products in your store by sending requests to the `/products` endpoint. Here are the available requests:

- `GET /products`: Get a list of all products in the store.
- `GET /products/<name>`: Get the details of a specific product.
- `POST /products`: Create a new product in the store. You need to provide the name, price, and quantity of the product in the body of the request.
- `PUT /products/<id>`: Update the details of a specific product. You can update the name, price, or quantity of the product in the body of the request.
- `DELETE /products/<id>`: Delete a specific product.


Creates a new product.

##### Request Body

| Field      | Type    | Description          |
| ---------- | ------- | -------------------- |
| name       | string  | The name of the product |
| price      | float   | The price of the product |
| quantity   | integer | The quantity of the product |


##### Response

| Field      | Type    | Description          |
| ---------- | ------- | -------------------- |
| id         | integer | The ID of the product  |
| name       | string  | The name of the product |
| price      | float   | The price of the product |
| quantity   | integer | The quantity of the product |

#### Update an existing product

##### Request Body

| Field      | Type    | Description          |
| ---------- | ------- | -------------------- |
| name       | string  | The name of the product |
| price      | float   | The price of the product |
| quantity   | integer | The quantity of the product |

##### Response

| Field      | Type    | Description          |
| ---------- | ------- | -------------------- |
| id         | integer | The ID of the product  |
| name       | string  | The name of the product |
| price      | float   | The price of the product |
| quantity   | integer | The quantity of the product |

## 💰 Managing Sales
You can manage the sales in your store by sending requests to the `/sales` endpoint. Here are the available requests:

- `GET /sales`: Get a list of all sales in the store.
- `GET /sales/<id>`: Get the details of a specific sale.
- `POST /sales`: Create a new sale in the store. You need to provide the product ID and the quantity of the product in the body of the request.
- `PUT /sales/<id>`: Update the details of a specific sale. You can update the product ID or the quantity of the sale in the body of the request.
- `DELETE /sales/<id>`: Delete a specific sale.

Creates a new sale.

##### Request Body

| Field      | Type    | Description          |
| ---------- | ------- | -------------------- |
| product_id | integer | The ID of the product being sold |
| quantity   | integer | The quantity of the product being sold |

##### Response

| Field      | Type    | Description          |
| ---------- | ------- | -------------------- |
| id         | integer | The ID of the sale  |
| user_id    | integer | The ID of the user making the sale |
| product_id | integer | The ID of the product being sold |
| date_sold  | string  | The date and time of the sale |
| total_sales| float   | The total sales amount |

## 📚 Dependencies

This API was built using the following dependencies:

- Flask: A micro web framework for Python.

- Flask-JWT-Extended: An extension for Flask that adds support for JSON Web Tokens (JWT) for authentication.
- SQLAlchemy: An Object-Relational Mapping (ORM) library for Python.


# Author: 
 [jck-bit](https://github.com/jck-bit)


## 📌 Contributing

Contributions to this project are always welcome!

# Badges

![Vercel](https://vercelbadge.vercel.app/api/[jck-bit]/[https://github.com/jck-bit/Stockify-Store-Management.git])