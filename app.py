import logging
from flask import Flask, request, jsonify, abort

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Sample Data
customers = []

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
    new_customer = {
        'id': len(customers) + 1,
        'name': data['name'],
        'email': data['email'],
        'phone_number': data['phone_number']
    }
    customers.append(new_customer)
    logging.info(f"Customer created: {new_customer}")
    return jsonify({'message': 'Customer created successfully', 'customer': new_customer}), 201

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = next((c for c in customers if c['id'] == id), None)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")
    logging.info(f"Customer retrieved: {customer}")
    return jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    if not data:
        logging.warning("Missing update data")
        abort(400, description="Missing update data")
    customer = next((c for c in customers if c['id'] == id), None)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")
    customer.update(data)
    logging.info(f"Customer updated: {customer}")
    return jsonify({'message': 'Customer updated successfully', 'customer': customer})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    global customers
    customer = next((c for c in customers if c['id'] == id), None)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")
    customers = [c for c in customers if c['id'] != id]
    logging.info(f"Customer deleted: {customer}")
    return jsonify({'message': 'Customer deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
