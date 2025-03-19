from flask import Flask, render_template, redirect, url_for, request, flash, session
from models import db, User, Product, Cart
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

# Create tables BEFORE any routes
with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('products'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Products Page
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash('Please login to add items to cart')
        return redirect(url_for('login'))
    
    quantity = int(request.form.get('quantity', 1))
    user_id = session['user_id']
    
    # Check if product already in cart
    existing_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart!')
    return redirect(url_for('cart'))

# Cart Page
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('Please login to view your cart')
        return redirect(url_for('login'))
    
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html',
                         cart_items=cart_items,
                         total_items=total_items,
                         total_price=total_price)

@app.route('/update_quantity/<int:cart_id>', methods=['POST'])
def update_quantity(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != session['user_id']:
        flash('Unauthorized action')
        return redirect(url_for('cart'))
    
    quantity = int(request.form['quantity'])
    if quantity > 0:
        cart_item.quantity = quantity
        db.session.commit()
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:cart_id>')
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != session['user_id']:
        flash('Unauthorized action')
        return redirect(url_for('cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Add your checkout logic here
    return render_template('checkout.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # This is where you'd normally integrate with a real payment gateway
    # For now, we'll just simulate a successful payment
    
    # Clear the user's cart after successful payment
    Cart.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    
    flash('Payment successful! Thank you for your purchase.')
    return redirect(url_for('products'))

@app.route('/empty_cart', methods=['POST'])
def empty_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Delete all cart items for the current user
    Cart.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    
    flash('Cart has been emptied')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
