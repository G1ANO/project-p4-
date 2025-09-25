from database import db, User, Plan, Subscription, bcrypt
from app import app  

with app.app_context():
   
    db.drop_all()
    db.create_all()

   
    basic = Plan(name="Basic", price=5.0, duration_minutes=60)
    premium = Plan(name="Premium", price=15.0, duration_minutes=300)
    db.session.add_all([basic, premium])
    db.session.commit()

   
    hashed_pw = bcrypt.generate_password_hash("password123").decode("utf-8")
    user = User(username="testuser", email="test@example.com", password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()

    
    sub = Subscription(user_id=user.id, plan_id=basic.id, status="active")
    db.session.add(sub)
    db.session.commit()

    print("✅ Database seeded with sample data!")
