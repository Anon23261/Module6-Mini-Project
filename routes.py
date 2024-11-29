from flask import request, jsonify
from app import app, db
from models import Customer, CustomerAccount, Product, Order

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

# CustomerAccount Management Endpoints

@app.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Customer account created successfully'}), 201

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get(id)
    if not account:
        return jsonify({'message': 'Customer account not found'}), 404
    return jsonify({'id': account.id, 'username': account.username, 'customer_id': account.customer_id})

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    data = request.get_json()
    account = CustomerAccount.query.get(id)
    if not account:
        return jsonify({'message': 'Customer account not found'}), 404
    account.username = data.get('username', account.username)
    account.password = data.get('password', account.password)
    db.session.commit()
    return jsonify({'message': 'Customer account updated successfully'})

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get(id)
    if not account:
        return jsonify({'message': 'Customer account not found'}), 404
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Customer account deleted successfully'})

# Product Catalog Management Endpoints

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], stock_level=data.get('stock_level', 0))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'stock_level': product.stock_level})

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock_level = data.get('stock_level', product.stock_level)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {'id': product.id, 'name': product.name, 'price': product.price, 'stock_level': product.stock_level}
        output.append(product_data)
    return jsonify(output)

# Bonus Features

@app.route('/products/<int:id>/stock', methods=['GET'])
def view_stock(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({'product_id': product.id, 'stock_level': product.stock_level})

@app.route('/products/<int:id>/stock', methods=['PUT'])
def update_stock(id):
    data = request.get_json()
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    product.stock_level = data.get('stock_level', product.stock_level)
    db.session.commit()
    return jsonify({'message': 'Stock level updated successfully'})

@app.route('/orders/<int:id>/total', methods=['GET'])
def calculate_order_total(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    # Calculate total price of the order
    total_price = 0
    for order_product in order.order_products:
        total_price += order_product.product.price * order_product.quantity
    return jsonify({'order_id': order.id, 'total_price': total_price})

# Order Processing Endpoints

@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(order_date=data['order_date'], customer_id=data['customer_id'])
    # Add logic to associate products with the order here
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    # Add logic to retrieve associated products here
    return jsonify({'id': order.id, 'order_date': order.order_date, 'customer_id': order.customer_id})

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.get_json()
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    # Add logic to update order details here
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})
