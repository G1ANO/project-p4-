from database import db, User, Plan, Subscription
from app import app  # import the Flask app so db knows the context

with app.app_context():
    # Clear old data (optional, but helps reset)
    db.drop_all()
    db.create_all()

    # ✅ Seed Plans
    basic = Plan(name="Basic", price=5.0, duration_minutes=60)
    premium = Plan(name="Premium", price=15.0, duration_minutes=300)
    db.session.add_all([basic, premium])
    db.session.commit()

    # ✅ Seed User
    user = User(username="testuser", email="test@example.com", password_hash="hashed_pw")
    db.session.add(user)
    db.session.commit()

    # ✅ Seed Subscription
    sub = Subscription(user_id=user.id, plan_id=basic.id, status="active")
    db.session.add(sub)
    db.session.commit()

    print("✅ Database seeded with sample data!")
