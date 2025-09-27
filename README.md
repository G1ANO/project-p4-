# WiFi Portal Subscription Management System

A modern full-stack web application for managing time-based WiFi access subscriptions. Built with Flask (Python) backend and React (JavaScript) frontend.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure registration and login with password validation
- **WiFi Plans**: Multiple time-based internet access plans
- **Subscription Management**: Purchase, view, and cancel subscriptions
-
### Security Features
- Password hashing with Werkzeug
- Email format validation with domain verification
- Password strength requirements (uppercase, lowercase, number/special character)
- Protected routes and authentication middleware
- CORS configuration for secure API access

## 📋 Available Plans

| Plan | Duration | Price |
|------|----------|-------|
| 1 Hour | 60 minutes | KSh 15 |
| 3 Hours | 180 minutes | KSh 25 |
| 6 Hours | 360 minutes | KSh 50 |
| 12 Hours | 720 minutes | KSh 100 |

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Marshmallow**: Data serialization/validation
- **SQLite**: Database (development)
- **Flask-CORS**: Cross-origin resource sharing
- **Werkzeug**: Password hashing

### Frontend
- **React**: JavaScript UI library
- **React Router**: Client-side routing
- **Vite**: Build tool and development server
- **CSS3**: Modern styling with flexbox/grid
- **Axios**: HTTP client for API requests

## 📁 Project Structure

```
wifi-portal/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── instance/
│       └── app.db         # SQLite database
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Nav.jsx    # Navigation component
│   │   ├── Pages/
│   │   │   ├── Login.jsx  # Login page
│   │   │   ├── Signup.jsx # Registration page
│   │   │   ├── Plans.jsx  # WiFi plans page
│   │   │   └── Subscriptions.jsx # Subscription management
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Application styles
│   │   └── main.jsx       # React entry point
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
└── README.md              # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```bash
   python app.py
   ```
   The database will be automatically created with sample plans.

4. **Start the Flask server**
   ```bash
   python app.py
   ```
   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## 🧪 Test Credentials

The application comes with pre-configured test users:

| Email | Password | Description |
|-------|----------|-------------|
| `user1@gmail.com` | `User1!` | Test user with valid credentials |
| `user2@gmail.com` | `Test2@` | Test user with valid credentials |

## 🎯 Usage Guide

### 1. User Registration/Login
- Visit `http://localhost:5173`
- Create account or login with test credentials
- Real-time validation ensures proper email/password format

### 2. Browse WiFi Plans
- After login, navigate to Plans page
- View available time-based internet access plans
- Subscribe to any plan with one click

### 3. Manage Subscriptions
- Visit Subscriptions page to view active subscriptions
- See purchase date, expiration time, and plan details
- Cancel subscriptions if needed
- Logout securely when done

## 🔧 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login

### Plans
- `GET /plans` - Get all available plans

### Subscriptions
- `GET /subscriptions/<user_id>` - Get user subscriptions
- `POST /subscriptions` - Create new subscription
- `DELETE /subscriptions/<subscription_id>` - Cancel subscription

### Users
- `GET /users` - Get all users (development only)

## 🎨 Design Features


## 🔒 Security Considerations

- Passwords are hashed using Werkzeug's secure methods
- Client-side validation prevents invalid data submission
- Protected routes ensure authenticated access only
- CORS properly configured for secure API communication
- Input sanitization and validation on both frontend and backend

## 🚀 Deployment

### Production Considerations
- Replace SQLite with PostgreSQL for production
- Set up environment variables for database configuration
- Configure proper CORS origins for production domains
- Implement rate limiting and additional security measures
- Set up SSL/HTTPS for secure communication

### Environment Variables
```bash
DATABASE_URI=postgresql://username:password@host:port/database
```

## 📝 License


## 👥 Contributors

- **Ian Muthiani** - Full-stack development
- **Donald Stephen** - Full-stack development

---

**Note**: 
