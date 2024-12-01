import logging
from flask import Flask, request, jsonify, abort
from models import db, Customer, CustomerAccount, Product

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    logging.info("Accessed home route")
    return "Welcome to the Customer Management API!"

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'phone_number')):
        logging.warning("Missing customer data")
        abort(400, description="Missing customer data")
    new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
    db.session.add(new_customer)
    db.session.commit()
    logging.info(f"Customer created: {new_customer}")
    return jsonify({'message': 'Customer created successfully', 'customer': {'id': new_customer.id, 'name': new_customer.name, 'email': new_customer.email, 'phone_number': new_customer.phone_number}}), 201

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")
    logging.info(f"Customer retrieved: {customer}")
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number})

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    if not data:
        logging.warning("Missing update data")
        abort(400, description="Missing update data")
    customer = Customer.query.get(id)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone_number = data.get('phone_number', customer.phone_number)
    db.session.commit()
    logging.info(f"Customer updated: {customer}")
    return jsonify({'message': 'Customer updated successfully', 'customer': {'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number}})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")
    db.session.delete(customer)
    db.session.commit()
    logging.info(f"Customer deleted: {customer}")
    return jsonify({'message': 'Customer deleted successfully'})

# CRUD routes for CustomerAccount
@app.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    if not data or not all(k in data for k in ('username', 'password', 'customer_id')):
        logging.warning("Missing customer account data")
        abort(400, description="Missing customer account data")
    new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
    db.session.add(new_account)
    db.session.commit()
    logging.info(f"CustomerAccount created: {new_account}")
    return jsonify({'message': 'CustomerAccount created successfully', 'account': {'id': new_account.id, 'username': new_account.username, 'customer_id': new_account.customer_id}}), 201

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get(id)
    if not account:
        logging.error(f"CustomerAccount with ID {id} not found")
        abort(404, description="CustomerAccount not found")
    logging.info(f"CustomerAccount retrieved: {account}")
    return jsonify({'id': account.id, 'username': account.username, 'customer_id': account.customer_id})

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    data = request.get_json()
    if not data:
        logging.warning("Missing update data")
        abort(400, description="Missing update data")
    account = CustomerAccount.query.get(id)
    if not account:
        logging.error(f"CustomerAccount with ID {id} not found")
        abort(404, description="CustomerAccount not found")
    account.username = data.get('username', account.username)
    account.password = data.get('password', account.password)
    db.session.commit()
    logging.info(f"CustomerAccount updated: {account}")
    return jsonify({'message': 'CustomerAccount updated successfully', 'account': {'id': account.id, 'username': account.username, 'customer_id': account.customer_id}})

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get(id)
    if not account:
        logging.error(f"CustomerAccount with ID {id} not found")
        abort(404, description="CustomerAccount not found")
    db.session.delete(account)
    db.session.commit()
    logging.info(f"CustomerAccount deleted: {account}")
    return jsonify({'message': 'CustomerAccount deleted successfully'})

# CRUD routes for Product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'price')):
        logging.warning("Missing product data")
        abort(400, description="Missing product data")
    new_product = Product(name=data['name'], price=data['price'], stock_level=data.get('stock_level', 0))
    db.session.add(new_product)
    db.session.commit()
    logging.info(f"Product created: {new_product}")
    return jsonify({'message': 'Product created successfully', 'product': {'id': new_product.id, 'name': new_product.name, 'price': new_product.price, 'stock_level': new_product.stock_level}}), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        logging.error(f"Product with ID {id} not found")
        abort(404, description="Product not found")
    logging.info(f"Product retrieved: {product}")
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'stock_level': product.stock_level})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    product_list = [{'id': p.id, 'name': p.name, 'price': p.price, 'stock_level': p.stock_level} for p in products]
    logging.info(f"Products listed: {product_list}")
    return jsonify(product_list)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    if not data:
        logging.warning("Missing update data")
        abort(400, description="Missing update data")
    product = Product.query.get(id)
    if not product:
        logging.error(f"Product with ID {id} not found")
        abort(404, description="Product not found")
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock_level = data.get('stock_level', product.stock_level)
    db.session.commit()
    logging.info(f"Product updated: {product}")
    return jsonify({'message': 'Product updated successfully', 'product': {'id': product.id, 'name': product.name, 'price': product.price, 'stock_level': product.stock_level}})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        logging.error(f"Product with ID {id} not found")
        abort(404, description="Product not found")
    db.session.delete(product)
    db.session.commit()
    logging.info(f"Product deleted: {product}")
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
