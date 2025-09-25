from app import app, db, Plan, User
from werkzeug.security import generate_password_hash

with app.app_context():
    print("=== DATABASE SETUP ===")
    
    # Create tables
    db.create_all()
    print("✅ Tables created")
    
    # Add sample data
    plan1 = Plan(name="Basic Plan", duration_minutes=60, price=1000)
    plan2 = Plan(name="Premium Plan", duration_minutes=1440, price=5000)
    
    db.session.add(plan1)
    db.session.add(plan2)
    db.session.commit()
    
    print("✅ Sample data added")
    
    # Verify
    plans_count = Plan.query.count()
    print(f"📊 Plans in database: {plans_count}")
