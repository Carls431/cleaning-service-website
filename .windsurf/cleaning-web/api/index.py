from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
import random
import string

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cleaning_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), default='default.jpg')
    category = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Service {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(10), unique=True, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    
    service = db.relationship('Service', backref=db.backref('bookings', lazy=True))
    
    def __repr__(self):
        return f'<Booking {self.booking_reference}>'

def generate_booking_reference():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Routes
@app.route('/')
def index():
    try:
        services = Service.query.all()
        return render_template('index.html', services=services)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/booking/<int:service_id>')
def booking(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        return render_template('booking.html', service=service)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/book', methods=['POST'])
def book():
    try:
        if request.method == 'POST':
            service_id = request.form.get('service_id')
            service = Service.query.get_or_404(service_id)
            
            booking_ref = generate_booking_reference()
            while Booking.query.filter_by(booking_reference=booking_ref).first():
                booking_ref = generate_booking_reference()
            
            booking_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
            booking_time = datetime.strptime(request.form.get('time'), '%H:%M').time()
            
            booking = Booking(
                booking_reference=booking_ref,
                service_id=service_id,
                customer_name=request.form.get('name'),
                customer_email=request.form.get('email'),
                customer_phone=request.form.get('phone'),
                customer_address=request.form.get('address'),
                booking_date=booking_date,
                booking_time=booking_time,
                total_price=service.price
            )
            
            db.session.add(booking)
            db.session.commit()
            
            flash(f'Booking successful! Your reference number is {booking_ref}', 'success')
            return redirect(url_for('confirmation', booking_ref=booking_ref))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/confirmation/<booking_ref>')
def confirmation(booking_ref):
    try:
        booking = Booking.query.filter_by(booking_reference=booking_ref).first_or_404()
        return render_template('confirmation.html', booking=booking)
    except Exception as e:
        return f"Error: {str(e)}", 500

# Initialize database
with app.app_context():
    try:
        db.create_all()
        
        if Service.query.count() == 0:
            sample_services = [
                Service(
                    name='Regular Cleaning',
                    description='Complete home cleaning including dusting, vacuuming, mopping, and bathroom cleaning',
                    price=89.99,
                    duration=3,
                    category='Regular',
                    image='regular-cleaning.jpg'
                ),
                Service(
                    name='Deep Cleaning',
                    description='Intensive cleaning service including detailed cleaning of all areas, inside cabinets, and hard-to-reach places',
                    price=199.99,
                    duration=6,
                    category='Deep',
                    image='deep-cleaning.jpg'
                ),
                Service(
                    name='Post-Construction Cleaning',
                    description='Professional cleaning after construction or renovation work',
                    price=299.99,
                    duration=8,
                    category='Special',
                    image='post-construction.jpg'
                ),
                Service(
                    name='Office Cleaning',
                    description='Commercial cleaning service for offices and workspaces',
                    price=149.99,
                    duration=4,
                    category='Commercial',
                    image='office-cleaning.jpg'
                )
            ]
            
            for service in sample_services:
                db.session.add(service)
            db.session.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")

# Vercel serverless function handler
def handler(environ, start_response):
    return app(environ, start_response)

# Export for Vercel
app_handler = app
