from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Enable CORS for frontend at 5173
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# ---------------------------
# MODELS
# ---------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id"), nullable=False)
    status = db.Column(db.String(50), default="active")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ends_at = db.Column(db.DateTime)

# ---------------------------
# SCHEMAS
# ---------------------------
class PlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Plan
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class SubscriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription
        load_instance = True
        include_fk = True

plan_schema = PlanSchema()
plans_schema = PlanSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)

# ---------------------------
# ROUTES
# ---------------------------

@app.route("/plans", methods=["GET"])
def get_plans():
    plans = Plan.query.all()
    return plans_schema.jsonify(plans)

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route("/subscriptions", methods=["POST"])
def create_subscription():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        user_id = data.get("user_id")
        plan_id = data.get("plan_id")

        if not user_id or not plan_id:
            return jsonify({"error": "user_id and plan_id required"}), 400

        user = db.session.get(User, user_id)
        plan = db.session.get(Plan, plan_id)

        if not user or not plan:
            return jsonify({"error": "Invalid user or plan"}), 400

        now = datetime.utcnow()
        ends_at = now + timedelta(minutes=plan.duration_minutes)

        sub = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            status="active",
            ends_at=ends_at,
            timestamp=now
        )

        db.session.add(sub)
        db.session.commit()

        return subscription_schema.jsonify(sub), 201

    except Exception as e:
        print("Error creating subscription:", str(e))  # logs in terminal
        return jsonify({"error": "Subscription failed", "details": str(e)}), 500


# ---------------------------
# NEW ROUTE: Get subscriptions for a user
# ---------------------------
@app.route("/subscriptions/<int:user_id>", methods=["GET"])
def get_user_subscriptions(user_id):
    subs = Subscription.query.filter_by(user_id=user_id).all()

    results = []
    for sub in subs:
        plan = db.session.get(Plan, sub.plan_id)
        results.append({
            "id": sub.id,
            "status": sub.status,
            "timestamp": sub.timestamp,
            "ends_at": sub.ends_at,
            "plan": {
                "id": plan.id,
                "name": plan.name,
                "duration_minutes": plan.duration_minutes,
                "price": plan.price
            }
        })

    return jsonify(results)

@app.route("/subscriptions/<int:sub_id>", methods=["DELETE"])
def delete_subscription(sub_id):
    sub = Subscription.query.get(sub_id)
    if not sub:
        return jsonify({"error": "Subscription not found"}), 404

    db.session.delete(sub)
    db.session.commit()
    return jsonify({"message": f"Subscription {sub_id} cancelled"}), 200


@app.route("/dashboard/<int:user_id>", methods=["GET"])
def get_dashboard(user_id):
    subs = Subscription.query.filter_by(user_id=user_id).all()
    
    dashboard_data = []
    for sub in subs:
        dashboard_data.append({
            "id": sub.id,
            "status": sub.status,
            "ends_at": sub.ends_at
        })
    
    return jsonify(dashboard_data), 200


# ---------------------------
# INIT DB
# ---------------------------
@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()

    # Seed sample data
    user1 = User(username="alice")
    user2 = User(username="bob")
    plan1 = Plan(name="Daily Pass", duration_minutes=1440, price=50)
    plan2 = Plan(name="Weekly Pass", duration_minutes=10080, price=300)
    db.session.add_all([user1, user2, plan1, plan2])
    db.session.commit()

    print("Database initialized with sample data.")

if __name__ == "__main__":
    app.run(debug=True)
