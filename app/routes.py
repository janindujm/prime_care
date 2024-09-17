# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import VehicleOwner, Payment, Service, ServiceProvider
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

@app.route('/carowner')
def carowner():
    return render_template('carowner.html')


@app.route('/service_provider')
def service_provider():
    return render_template('service_provider/service_provider.html')

@app.route('/service_provider_signup', methods=['GET', 'POST'])
def service_provider_signup():
    if request.method == 'POST':
        company_name = request.form['company_name']
        registration_number = request.form['registration_number']
        location = request.form['location']
        location_link = request.form['location_link']
        services = request.form.getlist('services')
        terms_and_conditions = request.form.get('terms_and_conditions')

        if not terms_and_conditions:
            flash("You must agree to the terms and conditions.", "danger")
            return render_template('service_provider_signup.html', error="You must agree to the terms and conditions.")
        
        # Add the new service provider
        new_provider = ServiceProvider(
            company_name=company_name,
            registration_number=registration_number,
            location=location,
            location_link=location_link,
            services=','.join(services)  # Store services as a comma-separated string
        )
        db.session.add(new_provider)
        db.session.commit()

        flash("Registration successful! Please log in to access your dashboard.", "success")
        return redirect(url_for('login'))

    services_list = [
        'Oil Change', 'Tire Rotation', 'Brake Inspection and Replacement',
        'Fluid Checks and Top-Offs', 'Air Filter Replacement', 'Battery Check and Replacement',
        'Spark Plug Replacement', 'Belt and Hose Inspection/Replacement', 'Transmission Fluid Change',
        'Alignment and Suspension Check', 'Cooling System Service', 'Headlight/Taillight Replacement',
        'Cabin Air Filter Replacement', 'Fuel System Cleaning', 'Exhaust System Inspection/Repair',
        'Wiper Blade Replacement', 'Timing Belt/Chain Replacement'
    ]

    return render_template('service_provider/service_provider_signup.html', services=services_list)