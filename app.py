from flask import Flask, request, jsonify
from db import db
from models import Customer, CustomerAccount, Product, Order
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()

# Customer Management Endpoints

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number})

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone_number = data.get('phone_number', customer.phone_number)
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

# Additional routes from routes.py can be added here following the same pattern.

if __name__ == '__main__':
    app.run(debug=True)
