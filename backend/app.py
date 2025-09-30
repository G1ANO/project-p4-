from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

app = Flask(__name__)

# Database configuration - PostgreSQL for production, SQLite for development
if os.environ.get("DATABASE_URL"):
    # Production: Use PostgreSQL from Render
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
else:
    # Development: Use SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

# CORS configuration for production
allowed_origins = [
    "http://localhost:5173",  # Development frontend
    "http://localhost:3000",  # Alternative dev port
    "https://project-p4-lovat.vercel.app",  # Production frontend
    os.environ.get("FRONTEND_URL", ""),  # Additional frontend URL from env
]

# Remove empty strings and add wildcard for development
allowed_origins = [origin for origin in allowed_origins if origin]
if not os.environ.get("FRONTEND_URL"):
    allowed_origins.append("*")  # Allow all origins in development

CORS(app, resources={
    r"/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

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
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ends_at = db.Column(db.DateTime)

class UserPlanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id"), nullable=False)
    purchase_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)

    user = db.relationship("User", backref="plan_history")
    plan = db.relationship("Plan", backref="user_history")


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

class UserPlanHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserPlanHistory
        load_instance = True
        include_fk = True

plan_schema = PlanSchema()
plans_schema = PlanSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)
user_plan_history_schema = UserPlanHistorySchema()
user_plan_histories_schema = UserPlanHistorySchema(many=True)


class RegisterResource(Resource):
    def post(self):
        data = request.json
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return {"message": "All fields are required"}, 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists"}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {
            "message": "User registered successfully",
            "user": {"id": new_user.id, "name": new_user.username, "email": new_user.email}
        }, 201

class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "Invalid credentials"}, 401

        if not bcrypt.check_password_hash(user.password_hash, password):
            return {"message": "Invalid credentials"}, 401

        return {"id": user.id, "name": user.username, "email": user.email}, 200

class PlansResource(Resource):
    def get(self):
        plans = Plan.query.all()
        return plans_schema.dump(plans), 200

class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users), 200

    def patch(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        db.session.commit()
        return user_schema.dump(user), 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

class SubscriptionsResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"error": "Missing JSON body"}, 400

            user_id = data.get("user_id")
            plan_id = data.get("plan_id")

            if not user_id or not plan_id:
                return {"error": "user_id and plan_id required"}, 400

            user = db.session.get(User, user_id)
            plan = db.session.get(Plan, plan_id)

            if not user or not plan:
                return {"error": "Invalid user or plan"}, 400

            # Check for existing active subscriptions that haven't expired
            now = datetime.now(timezone.utc)
            existing_active_sub = Subscription.query.filter(
                Subscription.user_id == user_id,
                Subscription.status == "active",
                Subscription.ends_at > now
            ).first()

            if existing_active_sub:
                # Ensure both datetimes are timezone-aware for comparison
                ends_at = existing_active_sub.ends_at
                if ends_at.tzinfo is None:
                    ends_at = ends_at.replace(tzinfo=timezone.utc)

                # Calculate remaining time
                remaining_time = ends_at - now
                hours = int(remaining_time.total_seconds() // 3600)
                minutes = int((remaining_time.total_seconds() % 3600) // 60)

                time_str = ""
                if hours > 0:
                    time_str += f"{hours} hour{'s' if hours > 1 else ''}"
                if minutes > 0:
                    if time_str:
                        time_str += f" and {minutes} minute{'s' if minutes > 1 else ''}"
                    else:
                        time_str = f"{minutes} minute{'s' if minutes > 1 else ''}"

                return {
                    "error": "You already have an active subscription",
                    "message": f"Your current subscription expires in {time_str}. Please wait until it expires before subscribing to a new plan.",
                    "current_subscription": {
                        "expires_at": existing_active_sub.ends_at.isoformat(),
                        "remaining_time": time_str
                    }
                }, 409  # Conflict status code

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

            # Also create UserPlanHistory entry
            history = UserPlanHistory(
                user_id=user.id,
                plan_id=plan.id,
                purchase_date=now
            )
            db.session.add(history)
            db.session.commit()

            return subscription_schema.dump(sub), 201

        except Exception as e:
            print("Error creating subscription:", str(e))
            return {"error": "Subscription failed", "details": str(e)}, 500

class UserSubscriptionsResource(Resource):
    def get(self, user_id):
        subs = Subscription.query.filter_by(user_id=user_id).all()
        results = []
        for sub in subs:
            plan = db.session.get(Plan, sub.plan_id)
            results.append({
                "id": sub.id,
                "status": sub.status,
                "timestamp": sub.timestamp.isoformat() if sub.timestamp else None,
                "ends_at": sub.ends_at.isoformat() if sub.ends_at else None,
                "plan": {
                    "id": plan.id,
                    "name": plan.name,
                    "duration_minutes": plan.duration_minutes,
                    "price": plan.price
                }
            })

        return results, 200

class SubscriptionResource(Resource):
    def delete(self, sub_id):
        sub = Subscription.query.get(sub_id)
        if not sub:
            return {"error": "Subscription not found"}, 404

        db.session.delete(sub)
        db.session.commit()
        return {"message": f"Subscription {sub_id} cancelled"}, 200

class UserPlanHistoryResource(Resource):
    def get(self, user_id):
        histories = UserPlanHistory.query.filter_by(user_id=user_id).all()
        return user_plan_histories_schema.dump(histories), 200

    def post(self):
        data = request.json
        user_id = data.get("user_id")
        plan_id = data.get("plan_id")
        rating = data.get("rating")
        review = data.get("review")

        if not user_id or not plan_id:
            return {"error": "user_id and plan_id required"}, 400

        history = UserPlanHistory(
            user_id=user_id,
            plan_id=plan_id,
            rating=rating,
            review=review
        )

        db.session.add(history)
        db.session.commit()

        return user_plan_history_schema.dump(history), 201

# Root endpoint for API health check
@app.route('/')
def api_root():
    return {
        "message": "WiFi Portal API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "register": "/register",
            "login": "/login",
            "plans": "/plans",
            "subscriptions": "/subscriptions",
            "users": "/users"
        }
    }

# Register API routes
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(PlansResource, '/plans')
api.add_resource(UsersResource, '/users', '/users/<int:user_id>')
api.add_resource(SubscriptionsResource, '/subscriptions')
api.add_resource(UserSubscriptionsResource, '/subscriptions/<int:user_id>')
api.add_resource(SubscriptionResource, '/subscriptions/<int:sub_id>')
api.add_resource(UserPlanHistoryResource, '/user-plan-history', '/user-plan-history/<int:user_id>')


@app.cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()

    # Create test users with valid credentials
    user1 = User(username="user1", email="user1@gmail.com", password_hash=bcrypt.generate_password_hash("User1!").decode('utf-8'))
    user2 = User(username="user2", email="user2@gmail.com", password_hash=bcrypt.generate_password_hash("Test2@").decode('utf-8'))

    # Create WiFi plans as specified
    plan1 = Plan(name="1 Hour", duration_minutes=60, price=15)
    plan2 = Plan(name="3 Hours", duration_minutes=180, price=25)
    plan3 = Plan(name="6 Hours", duration_minutes=360, price=50)
    plan4 = Plan(name="12 Hours", duration_minutes=720, price=100)

    db.session.add_all([user1, user2, plan1, plan2, plan3, plan4])
    db.session.commit()

    # Create sample UserPlanHistory entries
    history1 = UserPlanHistory(user_id=user1.id, plan_id=plan1.id, rating=5, review="Great service!")
    history2 = UserPlanHistory(user_id=user2.id, plan_id=plan2.id, rating=4, review="Good value for money")

    db.session.add_all([history1, history2])
    db.session.commit()

    print("Database initialized with sample data.")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)