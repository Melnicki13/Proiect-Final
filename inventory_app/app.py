from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, InventoryItem
from datetime import datetime
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        flash('Only administrators can register new users')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form

        # Validation
        if not username or not password:
            flash('Username and password are required')
            return redirect(url_for('register'))

        if len(username) < 3:
            flash('Username must be at least 3 characters long')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return redirect(url_for('register'))

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        # Create new user
        try:
            user = User(
                username=username,
                password=generate_password_hash(password),
                is_admin=is_admin
            )
            db.session.add(user)
            db.session.commit()
            flash('User registered successfully')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering the user')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    items = InventoryItem.query.all()
    return render_template('dashboard.html', items=items)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        item = InventoryItem(
            inventory_number=request.form['inventory_number'],
            company=request.form['company'],
            model=request.form['model'],
            purchase_year=int(request.form['purchase_year']),
            purchase_amount=float(request.form['purchase_amount']),
            department=request.form['department']
        )
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully')
        return redirect(url_for('dashboard'))
    return render_template('add_item.html')


@app.route('/delete_item/<int:id>')
@login_required
def delete_item(id):
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))

    item = InventoryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully')
    return redirect(url_for('dashboard'))


@app.route('/assign_item/<int:id>')
@login_required
def assign_item(id):
    item = InventoryItem.query.get_or_404(id)
    if item.assigned_user_id is None:
        item.assigned_user_id = current_user.id
        item.date_assigned = datetime.utcnow()
        db.session.commit()
        flash('Item assigned successfully')
    else:
        flash('Item is already assigned')
    return redirect(url_for('dashboard'))


@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '')
    items = InventoryItem.query.filter(
        (InventoryItem.company.contains(query)) |
        (InventoryItem.model.contains(query)) |
        (InventoryItem.inventory_number.contains(query))
    ).all()
    return render_template('dashboard.html', items=items)
def create_admin_if_not_exists():
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_if_not_exists()
    app.run(debug=True)