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
- Password hashing with Werkzeug
- Email format validation
- Password strength requirements (uppercase, lowercase, number/special character, max 10 chars)
- Protected routes and authentication middleware
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
- Werkzeug: Password hashing and security

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

# Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database migrations**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Start the Flask server**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

   The database will be automatically created with sample plans and users.

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies** (includes Formik & Yup)
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5174`

## 🧪 Test Credentials

The application comes with pre-configured test users:

| Email | Password | Description |
|-------|----------|-------------|
| `user1@gmail.com` | `User1!` | Test user with valid credentials |
| `user2@gmail.com` | `Test2@` | Test user with valid credentials |

# License


# Contributors

-Ian Muthiani - Full-stack developer
-Donald Kiarie- Full-stack developer
