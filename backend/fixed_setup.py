from app import app, db
from models import Plan, User, Subscription
from werkzeug.security import generate_password_hash

def setup_database():
    with app.app_context():
        print("Creating tables...")
        
        # Create all tables
        db.create_all()
        print("✅ Tables created!")
        
        # Clear any existing data
        try:
            User.query.delete()
            Plan.query.delete()
            db.session.commit()
            print("Cleared existing data")
        except:
            db.session.rollback()
            print("No data to clear")
        
        # Add sample data
        user1 = User(username="alice", email="alice@example.com", password_hash=generate_password_hash("password123"))
        user2 = User(username="bob", email="bob@example.com", password_hash=generate_password_hash("password123"))
        plan1 = Plan(name="Daily Pass", duration_minutes=1440, price=5000)
        plan2 = Plan(name="Weekly Pass", duration_minutes=10080, price=30000)
        plan3 = Plan(name="Monthly Pass", duration_minutes=43200, price=100000)
        
        db.session.add_all([user1, user2, plan1, plan2, plan3])
        db.session.commit()
        
        print("✅ Data added successfully!")
        print(f"Users: {User.query.count()}")
        print(f"Plans: {Plan.query.count()}")

if __name__ == "__main__":
    setup_database()
