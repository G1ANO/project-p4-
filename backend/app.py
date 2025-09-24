from flask import Flask, jsonify
from flask_cors import CORS
from database import db, ma, bcrypt, User, Plan, Subscription

def create_app():
    app = Flask(__name__)

    # ---------- CONFIG ----------
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key"  # ⚠️ change in production

    # ---------- INIT EXTENSIONS ----------
    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    # ---------- DB SETUP ----------
    with app.app_context():
        db.create_all()  # ✅ just ensures tables exist (no seeding here)

    # ---------- ROUTES ----------
    @app.route("/")
    def home():
        return {"message": "Flask is working! 🚀"}

    @app.route("/plans")
    def get_plans():
        plans = Plan.query.all()
        return jsonify([
            {"id": p.id, "name": p.name, "price": p.price, "duration_minutes": p.duration_minutes}
            for p in plans
        ])

    @app.route("/users")
    def get_users():
        users = User.query.all()
        return jsonify([
            {"id": u.id, "username": u.username, "email": u.email}
            for u in users
        ])

    @app.route("/subscriptions")
    def get_subscriptions():
        subs = Subscription.query.all()
        return jsonify([
            {
                "id": s.id,
                "user_id": s.user_id,
                "plan_id": s.plan_id,
                "status": s.status,
                "timestamp": s.timestamp
            }
            for s in subs
        ])

    return app


# Expose app for flask run
app = create_app()
