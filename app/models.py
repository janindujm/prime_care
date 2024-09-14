# app/models.py

from flask_login import UserMixin
from app import db
from datetime import datetime

class VehicleOwner(db.Model, UserMixin):  # Add UserMixin here directly
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    vehicle_brand = db.Column(db.String(100), nullable=False)
    vehicle_model = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    payments = db.relationship('Payment', backref='owner', lazy=True)
    services = db.relationship('Service', backref='owner', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('vehicle_owner.id'), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('vehicle_owner.id'), nullable=False)



class ServiceProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    location_link = db.Column(db.String(200), nullable=False)
    services = db.Column(db.Text, nullable=False)  # Store services as a comma-separated string
