from app import app, db, User, Plan
from werkzeug.security import generate_password_hash

with app.app_context():
    print("Adding sample data to PostgreSQL...")
    
    # Clear any existing data first
    try:
        User.query.delete()
        Plan.query.delete()
        db.session.commit()
        print("Cleared existing data")
    except:
        db.session.rollback()
        print("No existing data to clear")
    
    # Add sample users
    user1 = User(username="alice", email="alice@example.com", password_hash=generate_password_hash("password123"))
    user2 = User(username="bob", email="bob@example.com", password_hash=generate_password_hash("password123"))
    
    # Add sample plans (price in cents)
    plan1 = Plan(name="Daily Pass", duration_minutes=1440, price=5000)  # $50.00
    plan2 = Plan(name="Weekly Pass", duration_minutes=10080, price=30000)  # $300.00
    plan3 = Plan(name="Monthly Pass", duration_minutes=43200, price=100000)  # $1000.00
    
    db.session.add_all([user1, user2, plan1, plan2, plan3])
    db.session.commit()
    
    print("✅ Sample data added successfully!")
    print(f"Users: {User.query.count()}")
    print(f"Plans: {Plan.query.count()}")
