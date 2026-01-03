# CleanPro Cleaning Service Website

A professional cleaning service e-commerce website with booking system built with Python (Flask) and JavaScript.

## Features

### 🌟 Core Features
- **Beautiful Homepage**: Modern, responsive design with service showcase
- **Direct Booking System**: No user login required - simple booking process
- **Service Management**: Multiple cleaning services with pricing
- **Real-time Booking**: Date and time slot selection
- **Email Confirmations**: Automatic booking confirmations
- **Admin Dashboard**: Manage bookings and services
- **Mobile Responsive**: Works perfectly on all devices

### 🎨 Design Features
- Modern UI with gradient backgrounds
- Smooth animations and transitions
- Professional service cards
- Customer testimonials section
- Interactive contact forms
- Beautiful confirmation pages

### 🛠 Technical Features
- **Backend**: Python Flask framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 + Custom CSS
- **JavaScript**: Vanilla JS with modern features
- **Email**: Flask-Mail integration
- **Responsive**: Mobile-first design

## Project Structure

```
cleaning-web/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling
│   ├── js/
│   │   └── main.js        # Frontend JavaScript
│   └── images/            # Service images
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Homepage
    ├── booking.html       # Booking form
    ├── confirmation.html  # Booking confirmation
    └── admin/             # Admin templates
        ├── dashboard.html # Admin dashboard
        └── services.html # Service management
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd cleaning-web
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up email configuration** (optional)
   - Open `app.py`
   - Update the email configuration section with your SMTP details
   - For Gmail, you'll need to generate an App Password

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the website**
   - Open your browser and go to `http://localhost:5000`
   - Admin dashboard: `http://localhost:5000/admin`

## Usage

### For Customers
1. Browse services on the homepage
2. Click "Book This Service" on any service
3. Fill in the booking form with:
   - Preferred date and time
   - Contact information (name, email, phone)
   - Service address
   - Special instructions (optional)
4. Receive instant confirmation with reference number

### For Administrators
1. Access admin dashboard at `/admin`
2. View all bookings with status
3. Manage services (add/edit/remove)
4. Confirm or cancel bookings
5. Track revenue and statistics

## Configuration

### Email Setup (Optional)
To enable email confirmations, update these settings in `app.py`:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

### Database
The application uses SQLite by default. The database file (`cleaning_service.db`) will be created automatically when you first run the app.

### Customization
- **Services**: Edit the sample services in `app.py` or use the admin dashboard
- **Styling**: Modify `static/css/style.css` for custom colors and layout
- **Content**: Update HTML templates for text content changes

## Features in Detail

### Booking System
- **Service Selection**: Choose from various cleaning services
- **Date/Time Picker**: Interactive calendar and time slot selection
- **Customer Information**: Simple form with essential details only
- **Instant Confirmation**: Reference number generated immediately
- **Email Notifications**: Automatic confirmation emails (if configured)

### Admin Dashboard
- **Booking Management**: View, confirm, and cancel bookings
- **Service Management**: Add and edit cleaning services
- **Statistics**: Track total bookings and revenue
- **Status Updates**: Change booking statuses (pending, confirmed, cancelled)

### Responsive Design
- **Mobile-First**: Optimized for smartphones and tablets
- **Desktop Experience**: Enhanced layouts for larger screens
- **Touch-Friendly**: Easy navigation on touch devices
- **Fast Loading**: Optimized images and minimal JavaScript

## Sample Services Included

1. **Regular Cleaning** - ₱1,500 (3 hours)
   - Complete home cleaning including dusting, vacuuming, mopping, and bathroom cleaning

2. **Deep Cleaning** - ₱3,500 (6 hours)
   - Intensive cleaning with detailed attention to all areas

3. **Post-Construction Cleaning** - ₱5,000 (8 hours)
   - Professional cleaning after construction or renovation

4. **Office Cleaning** - ₱2,000 (4 hours)
   - Commercial cleaning for offices and workspaces

## Security Features

- **Form Validation**: Client-side and server-side validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **XSS Protection**: Jinja2 auto-escaping prevents XSS attacks
- **CSRF Protection**: Flask-WTF integration (if forms are extended)

## Future Enhancements

- **Payment Integration**: Stripe or PayPal integration
- **User Accounts**: Optional customer registration
- **SMS Notifications**: SMS confirmations and reminders
- **Multi-language Support**: Internationalization
- **Advanced Scheduling**: Recurring bookings and calendar integration
- **Mobile App**: Native mobile application
- **API Integration**: RESTful API for third-party integrations

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Try a different port
   python app.py --port 5001
   ```

2. **Email not working**
   - Check SMTP credentials
   - Ensure App Password is used for Gmail
   - Verify firewall settings

3. **Database errors**
   - Delete `cleaning_service.db` and restart the app
   - Check file permissions

4. **Images not loading**
   - Ensure images are in `static/images/` folder
   - Check file paths in templates

## Support

For support or questions:
- Email: info@cleanpro.com
- Phone: +63 912 345 6789

## License

This project is open source and available under the MIT License.

---

**CleanPro** - Professional Cleaning Services Made Easy 🧹✨
