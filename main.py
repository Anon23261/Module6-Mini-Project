import logging
from flask import Flask, request, jsonify, abort
from models import db, Customer, CustomerAccount, Product, Order

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_management.db'
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

# Customer Routes
@app.route('/customers', methods=['GET', 'POST'])
def customers_handler():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'phone_number')):
            logging.warning("Missing customer data")
            abort(400, description="Missing customer data")
        new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
        db.session.add(new_customer)
        db.session.commit()
        logging.info(f"Customer created: {new_customer}")
        return jsonify({'message': 'Customer created successfully', 'customer': {'id': new_customer.id, 'name': new_customer.name, 'email': new_customer.email, 'phone_number': new_customer.phone_number}}), 201
    elif request.method == 'GET':
        customers = Customer.query.all()
        return jsonify([{'id': c.id, 'name': c.name, 'email': c.email, 'phone_number': c.phone_number} for c in customers])

@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customer_handler(id):
    customer = Customer.query.get(id)
    if not customer:
        logging.error(f"Customer with ID {id} not found")
        abort(404, description="Customer not found")

    if request.method == 'GET':
        logging.info(f"Customer retrieved: {customer}")
        return jsonify({'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number})
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            logging.warning("Missing update data")
            abort(400, description="No update data provided")
        
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone_number' in data:
            customer.phone_number = data['phone_number']
        
        db.session.commit()
        logging.info(f"Customer updated: {customer}")
        return jsonify({'message': 'Customer updated successfully', 'customer': {'id': customer.id, 'name': customer.name, 'email': customer.email, 'phone_number': customer.phone_number}})
    
    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        logging.info(f"Customer deleted: {customer}")
        return jsonify({'message': 'Customer deleted successfully'})

# Customer Account Routes
@app.route('/customer-accounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    if not data or not all(k in data for k in ('customer_id', 'username', 'password')):
        logging.warning("Missing customer account data")
        abort(400, description="Missing customer account data")
    new_account = CustomerAccount(
        customer_id=data['customer_id'],
        username=data['username'],
        password=data['password']
    )
    db.session.add(new_account)
    db.session.commit()
    logging.info(f"Customer account created: {new_account}")
    return jsonify({
        'message': 'Customer account created successfully',
        'account': {
            'id': new_account.id,
            'customer_id': new_account.customer_id,
            'username': new_account.username
        }
    }), 201

@app.route('/customer-accounts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customer_account_handler(id):
    account = CustomerAccount.query.get(id)
    if not account:
        logging.error(f"Customer account with ID {id} not found")
        abort(404, description="Customer account not found")

    if request.method == 'GET':
        logging.info(f"Customer account retrieved: {account}")
        return jsonify({
            'id': account.id,
            'customer_id': account.customer_id,
            'username': account.username
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            logging.warning("Missing update data")
            abort(400, description="No update data provided")
        
        if 'username' in data:
            account.username = data['username']
        if 'password' in data:
            account.password = data['password']
        
        db.session.commit()
        logging.info(f"Customer account updated: {account}")
        return jsonify({
            'message': 'Customer account updated successfully',
            'account': {
                'id': account.id,
                'customer_id': account.customer_id,
                'username': account.username
            }
        })
    
    elif request.method == 'DELETE':
        db.session.delete(account)
        db.session.commit()
        logging.info(f"Customer account deleted: {account}")
        return jsonify({'message': 'Customer account deleted successfully'})

# Order Routes
@app.route('/orders', methods=['GET', 'POST'])
def orders_handler():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('customer_id', 'product_id', 'quantity')):
            logging.warning("Missing order data")
            abort(400, description="Missing order data")
        new_order = Order(
            customer_id=data['customer_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            status='pending'
        )
        db.session.add(new_order)
        db.session.commit()
        logging.info(f"Order created: {new_order}")
        return jsonify({
            'message': 'Order created successfully',
            'order': {
                'id': new_order.id,
                'customer_id': new_order.customer_id,
                'product_id': new_order.product_id,
                'quantity': new_order.quantity,
                'status': new_order.status
            }
        }), 201
    elif request.method == 'GET':
        orders = Order.query.all()
        return jsonify([{
            'id': o.id,
            'customer_id': o.customer_id,
            'product_id': o.product_id,
            'quantity': o.quantity,
            'status': o.status
        } for o in orders])

@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def order_handler(id):
    order = Order.query.get(id)
    if not order:
        logging.error(f"Order with ID {id} not found")
        abort(404, description="Order not found")

    if request.method == 'GET':
        logging.info(f"Order retrieved: {order}")
        return jsonify({
            'id': order.id,
            'customer_id': order.customer_id,
            'product_id': order.product_id,
            'quantity': order.quantity,
            'status': order.status
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            logging.warning("Missing update data")
            abort(400, description="No update data provided")
        
        if 'status' in data:
            order.status = data['status']
        if 'quantity' in data:
            order.quantity = data['quantity']
        
        db.session.commit()
        logging.info(f"Order updated: {order}")
        return jsonify({
            'message': 'Order updated successfully',
            'order': {
                'id': order.id,
                'customer_id': order.customer_id,
                'product_id': order.product_id,
                'quantity': order.quantity,
                'status': order.status
            }
        })
    
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        logging.info(f"Order deleted: {order}")
        return jsonify({'message': 'Order deleted successfully'})

# Product Routes
@app.route('/products', methods=['GET', 'POST'])
def products_handler():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'price', 'stock_level')):
            logging.warning("Missing product data")
            abort(400, description="Missing product data")
        new_product = Product(
            name=data['name'],
            price=data['price'],
            stock_level=data['stock_level']
        )
        db.session.add(new_product)
        db.session.commit()
        logging.info(f"Product created: {new_product}")
        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'id': new_product.id,
                'name': new_product.name,
                'price': new_product.price,
                'stock_level': new_product.stock_level
            }
        }), 201
    elif request.method == 'GET':
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'stock_level': p.stock_level
        } for p in products])

@app.route('/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product_handler(id):
    product = Product.query.get(id)
    if not product:
        logging.error(f"Product with ID {id} not found")
        abort(404, description="Product not found")

    if request.method == 'GET':
        logging.info(f"Product retrieved: {product}")
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock_level': product.stock_level
        })
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            logging.warning("Missing update data")
            abort(400, description="No update data provided")
        
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'stock_level' in data:
            product.stock_level = data['stock_level']
        
        db.session.commit()
        logging.info(f"Product updated: {product}")
        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock_level': product.stock_level
            }
        })
    
    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        logging.info(f"Product deleted: {product}")
        return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
