# routes.py

from flask import Flask, request, jsonify, abort
from models import customers, orders
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Define routes
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Customer Management API!"

@app.route('/customers', methods=['GET', 'POST'])
def customers_handler():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'phone_number')):
            logging.warning("Missing customer data")
            abort(400, description="Missing customer data")
        new_customer = {
            'id': len(customers) + 1,
            'name': data['name'],
            'email': data['email'],
            'phone_number': data['phone_number']
        }
        customers.append(new_customer)
        logging.info(f"Customer created: {new_customer}")
        return jsonify({'message': 'Customer created successfully', 'customer': new_customer}), 201
    elif request.method == 'GET':
        return jsonify(customers)

@app.route('/customers/<int:id>', methods=['GET', 'DELETE'])
def customer_handler(id):
    if request.method == 'GET':
        customer = next((c for c in customers if c['id'] == id), None)
        if not customer:
            logging.error(f"Customer with ID {id} not found")
            abort(404, description="Customer not found")
        logging.info(f"Customer retrieved: {customer}")
        return jsonify(customer)
    else:
        customer = next((c for c in customers if c['id'] == id), None)
        if not customer:
            logging.error(f"Customer with ID {id} not found")
            abort(404, description="Customer not found")
        customers = [c for c in customers if c['id'] != id]
        logging.info(f"Customer deleted: {customer}")
        return jsonify({'message': 'Customer deleted successfully'})

@app.route('/orders', methods=['GET', 'POST'])
def orders_handler():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('customer_id', 'product_id', 'quantity', 'status')):
            logging.warning("Missing order data")
            abort(400, description="Missing order data")
        new_order = {
            'id': len(orders) + 1,
            'customer_id': data['customer_id'],
            'product_id': data['product_id'],
            'quantity': data['quantity'],
            'status': data['status']
        }
        orders.append(new_order)
        logging.info(f"Order created: {new_order}")
        return jsonify({'message': 'Order created successfully', 'order': new_order}), 201
    elif request.method == 'GET':
        return jsonify(orders)

@app.route('/orders/<int:id>', methods=['GET', 'DELETE'])
def order_handler(id):
    order = next((o for o in orders if o['id'] == id), None)
    if not order:
        logging.warning(f"Order not found: {id}")
        abort(404, description="Order not found")
    if request.method == 'GET':
        return jsonify(order)
    elif request.method == 'DELETE':
        orders.remove(order)
        logging.info(f"Order deleted: {id}")
        return jsonify({'message': 'Order deleted successfully'})
