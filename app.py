import logging
from flask import Flask, request, jsonify, abort
from models import db, Customer, CustomerAccount, Product
from flask_caching import Cache
from datetime import datetime
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure Flask-Caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:your_password@localhost/customer_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

# Initialize extensions
db.init_app(app)
cache.init_app(app)

def handle_error(e):
    logger.error(f"Error: {str(e)}\n{traceback.format_exc()}")
    return jsonify(error=str(e)), getattr(e, 'code', 500)

@app.errorhandler(404)
def not_found_error(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(400)
def bad_request_error(e):
    return jsonify(error=str(e.description)), 400

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return jsonify(error="Internal server error"), 500

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    logger.info("Accessed home route")
    return jsonify({"message": "Welcome to the Customer Management API!", 
                   "version": "1.0",
                   "endpoints": [
                       "/customers",
                       "/customer_accounts",
                       "/products"
                   ]})

@app.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'phone_number')):
            logger.warning("Missing customer data")
            abort(400, description="Missing customer data")
        
        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number']
        )
        db.session.add(new_customer)
        db.session.commit()
        
        logger.info(f"Customer created: {new_customer.to_dict()}")
        return jsonify({
            'message': 'Customer created successfully',
            'customer': new_customer.to_dict()
        }), 201
    except Exception as e:
        return handle_error(e)

@app.route('/customers/<int:id>', methods=['GET'])
@cache.memoize(timeout=60)
def get_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        logger.info(f"Customer retrieved: {customer.to_dict()}")
        return jsonify(customer.to_dict())
    except Exception as e:
        return handle_error(e)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        data = request.get_json()
        if not data:
            logger.warning("Missing update data")
            abort(400, description="Missing update data")
        customer = Customer.query.get_or_404(id)
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone_number = data.get('phone_number', customer.phone_number)
        db.session.commit()
        logger.info(f"Customer updated: {customer.to_dict()}")
        return jsonify({
            'message': 'Customer updated successfully',
            'customer': customer.to_dict()
        })
    except Exception as e:
        return handle_error(e)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        logger.info(f"Customer deleted: {customer.to_dict()}")
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        return handle_error(e)

@app.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('username', 'password', 'customer_id')):
            logger.warning("Missing customer account data")
            abort(400, description="Missing customer account data")
        new_account = CustomerAccount(
            username=data['username'],
            password=data['password'],
            customer_id=data['customer_id']
        )
        db.session.add(new_account)
        db.session.commit()
        logger.info(f"CustomerAccount created: {new_account.to_dict()}")
        return jsonify({
            'message': 'CustomerAccount created successfully',
            'account': new_account.to_dict()
        }), 201
    except Exception as e:
        return handle_error(e)

@app.route('/customer_accounts/<int:id>', methods=['GET'])
@cache.memoize(timeout=60)
def get_customer_account(id):
    try:
        account = CustomerAccount.query.get_or_404(id)
        logger.info(f"CustomerAccount retrieved: {account.to_dict()}")
        return jsonify(account.to_dict())
    except Exception as e:
        return handle_error(e)

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    try:
        data = request.get_json()
        if not data:
            logger.warning("Missing update data")
            abort(400, description="Missing update data")
        account = CustomerAccount.query.get_or_404(id)
        account.username = data.get('username', account.username)
        account.password = data.get('password', account.password)
        db.session.commit()
        logger.info(f"CustomerAccount updated: {account.to_dict()}")
        return jsonify({
            'message': 'CustomerAccount updated successfully',
            'account': account.to_dict()
        })
    except Exception as e:
        return handle_error(e)

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    try:
        account = CustomerAccount.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        logger.info(f"CustomerAccount deleted: {account.to_dict()}")
        return jsonify({'message': 'CustomerAccount deleted successfully'})
    except Exception as e:
        return handle_error(e)

@app.route('/products', methods=['GET'])
@cache.cached(timeout=60)
def list_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        return handle_error(e)

@app.route('/products/<int:id>', methods=['GET'])
@cache.memoize(timeout=60)
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict())
    except Exception as e:
        return handle_error(e)

@app.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'price')):
            abort(400, description="Missing product data")
        
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock_level=data.get('stock_level', 0)
        )
        db.session.add(new_product)
        db.session.commit()
        cache.delete_memoized(list_products)
        
        return jsonify({
            'message': 'Product created successfully',
            'product': new_product.to_dict()
        }), 201
    except Exception as e:
        return handle_error(e)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()
        if not data:
            logger.warning("Missing update data")
            abort(400, description="Missing update data")
        product = Product.query.get_or_404(id)
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock_level = data.get('stock_level', product.stock_level)
        db.session.commit()
        cache.delete_memoized(list_products)
        logger.info(f"Product updated: {product.to_dict()}")
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        })
    except Exception as e:
        return handle_error(e)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        cache.delete_memoized(list_products)
        logger.info(f"Product deleted: {product.to_dict()}")
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        return handle_error(e)

if __name__ == '__main__':
    app.run(debug=True)
