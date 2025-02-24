# Importăm modulele necesare
from flask_sqlalchemy import SQLAlchemy # Pentru baza de date
from flask_login import UserMixin # Pentru gestionarea utilizatorilor
from datetime import datetime # Pentru timestamping


# Inițializăm obiectul SQLAlchemy
db = SQLAlchemy()
# Definim modelul User care moștenește UserMixin pentru
# funcționalități de autentificare


class User(UserMixin, db.Model):  # Definim coloana ID ca cheie primară
    id = db.Column(db.Integer, primary_key=True)
# Coloana pentru nume utilizator, unic și obligatoriu
    username = db.Column(db.String(80), unique=True, nullable=False)
# Coloana pentru parolă, obligatorie
    password = db.Column(db.String(120), nullable=False)
# Coloana pentru rol administrator (boolean)
    is_admin = db.Column(db.Boolean, default=False)
# Relație one-to-many cu InventoryItem
    items_assigned = db.relationship('InventoryItem', backref='assigned_to', lazy=True)


# Definim modelul pentru obiectele din inventar
class InventoryItem(db.Model):
    # Definim coloana ID ca cheie primară
    id = db.Column(db.Integer, primary_key=True)
    # Numărul de inventar, unic și obligatoriu
    inventory_number = db.Column(db.String(50), unique=True, nullable=False)
    # Firma producătoare
    company = db.Column(db.String(100), nullable=False)
    # Modelul produsului
    model = db.Column(db.String(100), nullable=False)
    # Anul achiziției
    purchase_year = db.Column(db.Integer, nullable=False)
    # Suma de achiziție
    purchase_amount = db.Column(db.Float, nullable=False)
    # Departamentul
    department = db.Column(db.String(100), nullable=False)
    # Cheie străină pentru utilizatorul care are itemul alocat
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # Data alocării
    date_assigned = db.Column(db.DateTime, nullable=True)
