# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import VehicleOwner, Payment, Service
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return VehicleOwner.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        vehicle_brand = request.form['vehicle_brand']
        vehicle_model = request.form['vehicle_model']
        location = request.form['location']

        # Add the new user
        new_owner = VehicleOwner(
            first_name=first_name,
            second_name=second_name,
            contact_number=contact_number,
            email=email,
            vehicle_brand=vehicle_brand,
            vehicle_model=vehicle_model,
            location=location
        )
        db.session.add(new_owner)
        db.session.commit()

        flash("Registration successful! Please log in to access your dashboard.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = VehicleOwner.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login failed. Check your email and try again.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    owner = VehicleOwner.query.filter_by(email=current_user.email).first()
    payments = Payment.query.filter_by(owner_id=owner.id).all()
    services = Service.query.filter_by(owner_id=owner.id).all()

    return render_template('dashboard.html', owner=owner, payments=payments, services=services)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


