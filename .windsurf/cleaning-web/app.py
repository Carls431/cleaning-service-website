from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
import random
import string

app = Flask(__name__)
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
    duration = db.Column(db.Integer, nullable=False)  # in hours
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
    services = Service.query.all()
    return render_template('index.html', services=services)

@app.route('/booking/<int:service_id>')
def booking(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template('booking.html', service=service)

@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        service = Service.query.get_or_404(service_id)
        
        # Generate unique booking reference
        booking_ref = generate_booking_reference()
        while Booking.query.filter_by(booking_reference=booking_ref).first():
            booking_ref = generate_booking_reference()
        
        # Parse date and time
        booking_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        booking_time = datetime.strptime(request.form.get('time'), '%H:%M').time()
        
        # Create new booking
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
        
        # Send confirmation email (optional - requires email setup)
        try:
            send_confirmation_email(booking)
        except:
            pass  # Continue even if email fails
        
        flash(f'Booking successful! Your reference number is {booking_ref}', 'success')
        return redirect(url_for('confirmation', booking_ref=booking_ref))

@app.route('/confirmation/<booking_ref>')
def confirmation(booking_ref):
    booking = Booking.query.filter_by(booking_reference=booking_ref).first_or_404()
    return render_template('confirmation.html', booking=booking)

@app.route('/admin')
def admin():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/dashboard.html', bookings=bookings)

@app.route('/admin/services')
def admin_services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@app.route('/admin/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        service = Service(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            duration=int(request.form.get('duration')),
            category=request.form.get('category'),
            image=request.form.get('image', 'default.jpg')
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin_services'))
    return render_template('admin/add_service.html')

def send_confirmation_email(booking):
    msg = Message(
        'Cleaning Service Booking Confirmation',
        sender='your-email@gmail.com',
        recipients=[booking.customer_email]
    )
    msg.body = f'''
    Dear {booking.customer_name},
    
    Thank you for booking our cleaning service!
    
    Booking Reference: {booking.booking_reference}
    Service: {booking.service.name}
    Date: {booking.booking_date}
    Time: {booking.booking_time}
    Address: {booking.customer_address}
    Total Price: ₱{booking.total_price}
    
    We will contact you soon to confirm your booking.
    
    Best regards,
    Cleaning Service Team
    '''
    mail.send(msg)

# Initialize database
with app.app_context():
    db.create_all()
    
    # Add sample services if database is empty
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

@app.route('/admin/confirm/<int:booking_id>', methods=['POST'])
def confirm_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'confirmed'
    db.session.commit()
    return jsonify({'success': True, 'message': 'Booking confirmed successfully'})

@app.route('/admin/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'cancelled'
    db.session.commit()
    return jsonify({'success': True, 'message': 'Booking cancelled successfully'})

@app.route('/admin/booking/<int:booking_id>')
def get_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return jsonify({
        'id': booking.id,
        'booking_reference': booking.booking_reference,
        'customer_name': booking.customer_name,
        'customer_email': booking.customer_email,
        'customer_phone': booking.customer_phone,
        'customer_address': booking.customer_address,
        'service_name': booking.service.name,
        'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
        'booking_time': booking.booking_time.strftime('%H:%M'),
        'status': booking.status,
        'total_price': booking.total_price
    })

if __name__ == '__main__':
    app.run(debug=True)
