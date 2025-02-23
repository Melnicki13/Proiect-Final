from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    items_assigned = db.relationship('InventoryItem', backref='assigned_to', lazy=True)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_number = db.Column(db.String(50), unique=True, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    purchase_year = db.Column(db.Integer, nullable=False)
    purchase_amount = db.Column(db.Float, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_assigned = db.Column(db.DateTime, nullable=True)
