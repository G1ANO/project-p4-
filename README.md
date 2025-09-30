# WiFi Portal Subscription Management System

A web application for managing time-based WiFi access subscriptions. Built with Flask (Python) backend and React (JavaScript) frontend.

# Features

-User Authentication: Secure registration and login with Formik validation
-WiFi Plans: Multiple time-based internet access plans
-Subscription Management: Purchase, view, and cancel subscriptions
-Real-time Validation: Client-side form validati0n
-Formik Forms: Advanced form handling with Yup validation schemas
-Database Relationships:
  - One-to-Many relationships (User→Subscription, Plan→Subscription)
  - Many-to-Many relationship (User↔Plan via UserPlanHistory)
-Full CRUD Operations: Complete Create, Read, Update, Delete functionality
-Database Migrations: Flask-Migrate for schema management

# Security Features
- Password hashing with Flask-Bcrypt
- Email format validation
- Password strength requirements (uppercase, lowercase, number/special character, max 10 chars)
- CORS configuration for secure API access

# Technology Stack

#  Backend
- Flask: Python web framework
- Flask-RESTful: REST API framework with Resource classes
- Flask-Migrate: Database migration management
- SQLAlchemy: Database ORM with relationship modeling
- Marshmallow: Data serialization andvalidation
- SQLite: Database (development)
- Flask-CORS: Cross-origin resource sharing
- Flask-Bcrypt: Secure password hashing and verification

# Frontend
- React: JavaScript UI library
- React Router: Client-side routing
- Formik: Advanced form handling and validation
- Yup: Schema validation for forms
- Vite: Build tool and development server
- CSS: Styling
- Axios/Fetch

# Project Structure
```
├── backend/
│   ├── app.py              # Main Flask-RESTful application
│   ├── requirements.txt    # Python dependencies
│   ├── migrations/         # Flask-Migrate database migrations
│   │   ├── versions/       # Migration version files
│   │   ├── alembic.ini     # Alembic configuration
│   │   └── env.py          # Migration environment
│   └── instance/
│       └── app.db         # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Nav.jsx    # Navigation component
│   │   ├── Pages/
│   │   │   ├── Login.jsx  # Formik login form
│   │   │   ├── Signup.jsx # Formik registration form
│   │   │   ├── Plans.jsx  # WiFi plans page
│   │   │   └── Subscriptions.jsx # Subscription management
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Application styles
│   │   └── main.jsx       # React entry point
│   ├── package.json       # Node.js dependencies (includes Formik & Yup)
│   └── vite.config.js     # Vite configuration
└── README.md              # Project documentation
```

# Quick Start

# Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- WiFi Router/Hotspot with captive portal capability (for production)
- Payment gateway account (PayPal, M-Pesa, etc.) (for production)

# Deployment Status
Frontend (React):
 https://project-p4-lovat.vercel.app/
Backend API (Flask):
 https://project-p4-yc0o.onrender.com/


# Test Credentials

The application comes with pre-configured test users:

 Email | Password
 user1@gmail.com | User1!
 user2@gmail.com | Test2@

### Quick Test:
1. Visit the [login page]
2. Use test credentials above
3. Browse plans and try subscribing
4. Check subscriptions page


## WiFi Hotspot/Router Configuration

To deploy this system as a real WiFi portal, you need to configure your router or hotspot to redirect users to the login page:

# 1. Captive Portal Setup
Configure your WiFi router to redirect all HTTP requests and DNS queries to your portal

# 2. Firewall Rules
Block internet access until payment is confirmed

# Payment Gateway Integration

Integrate payment methods such as PayPal and M-Pesa STK Push Implementation after pressing purchase on a plan.

## Network Access Control

After successful payment, grant internet access.

## Hardware Requirements

### Recommended Setup:
- Router: OpenWrt-compatible router (e.g., TP-Link Archer C7)
- Server: Raspberry Pi 4 or dedicated server
- Network: Separate VLAN for guest access

# Alternative Solutions:
- Cloud Hosting: Deploy on AWS/DigitalOcean with VPN to router
- Mikrotik RouterOS: Built-in hotspot functionality

# License

This project is under MIT Liscence validation and is open for legal persoal, commercial, and educational use.

# CREDITS

-IAN MUTHIANI
Full-stack developer

-DONALD KIARIE
 Full-stack developer
