from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"   # 🔹 double underscores

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    subscriptions = db.relationship("Subscription", back_populates="user")

class Plan(db.Model):
    __tablename__ = "plans"   # 🔹 double underscores

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)

    subscriptions = db.relationship("Subscription", back_populates="plan")

class Subscription(db.Model):
    __tablename__ = "subscriptions"   # 🔹 double underscores

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"))
    status = db.Column(db.String(20), default="active")
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", back_populates="subscriptions")
    plan = db.relationship("Plan", back_populates="subscriptions")
