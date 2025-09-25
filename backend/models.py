from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, ma, bcrypt, User, Plan, Subscription
from marshmallow import validates, ValidationError, fields
from datetime import datetime, timedelta

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "super-secret-key"

    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()
        # Seed default plans if none exist
        if Plan.query.count() == 0:
            basic = Plan(name="Basic", price=5.0, duration_minutes=60)
            premium = Plan(name="Premium", price=15.0, duration_minutes=300)
            db.session.add_all([basic, premium])
            db.session.commit()

    # =====================
    # Schemas
    # =====================
    class UserSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = User
            load_instance = True
            exclude = ("password_hash",)
            include_fk = True

        email = fields.Email(required=True)
        username = fields.Str(required=True)
        password = fields.Str(load_only=True, required=True)

        @validates("password")
        def validate_password(self, value):
            if len(value) < 6:
                raise ValidationError("Password must be at least 6 characters long.")

    class PlanSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Plan
            load_instance = True

    class SubscriptionSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Subscription
            load_instance = True
            include_fk = True

        plan_name = fields.Method("get_plan_name")
        time_bought = fields.Method("get_time_bought")
        time_ends = fields.Method("get_time_ends")

        def get_plan_name(self, obj):
            return obj.plan.name if obj.plan else None

        def get_time_bought(self, obj):
            return obj.timestamp.isoformat() if obj.timestamp else None

        def get_time_ends(self, obj):
            return obj.ends_at.isoformat() if obj.ends_at else None

    user_schema = UserSchema()
    users_schema = UserSchema(many=True)
    plan_schema = PlanSchema()
    plans_schema = PlanSchema(many=True)
    subscription_schema = SubscriptionSchema()
    subscriptions_schema = SubscriptionSchema(many=True)

    
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return jsonify(errors), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 400

        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = User(
            username=data["username"],
            email=data["email"],
            password_hash=hashed_pw
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data.get("email")).first()
        if user and bcrypt.check_password_hash(user.password_hash, data.get("password")):
            return user_schema.jsonify(user), 200
        return jsonify({"error": "Invalid email or password"}), 401

    @app.route("/plans", methods=["GET"])
    def get_plans():
        plans = Plan.query.all()
        return plans_schema.jsonify(plans), 200

    @app.route("/subscriptions/<int:user_id>", methods=["GET"])
    def get_user_subscriptions(user_id):
        subs = Subscription.query.filter_by(user_id=user_id).all()
        return subscriptions_schema.jsonify(subs), 200

    @app.route("/subscriptions", methods=["POST"])
    def create_subscription():
        data = request.get_json()
        user = User.query.get(data.get("user_id"))
        plan = Plan.query.get(data.get("plan_id"))

        if not user or not plan:
            return jsonify({"error": "Invalid user or plan"}), 400

        timestamp = datetime.utcnow()
        ends_at = timestamp + timedelta(minutes=plan.duration_minutes)

        sub = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            status="active",
            timestamp=timestamp,
            ends_at=ends_at
        )
        db.session.add(sub)
        db.session.commit()

        return subscription_schema.jsonify(sub), 201

    @app.route("/subscriptions/<int:sub_id>", methods=["DELETE"])
    def cancel_subscription(sub_id):
        sub = Subscription.query.get(sub_id)
        if not sub:
            return jsonify({"error": "Subscription not found"}), 404

        sub.status = "cancelled"  # mark as cancelled
        db.session.commit()
        return subscription_schema.jsonify(sub), 200

    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        stats = [
            {"id": 1, "title": "Total Users", "value": User.query.count()},
            {"id": 2, "title": "Total Plans", "value": Plan.query.count()},
            {"id": 3, "title": "Total Subscriptions", "value": Subscription.query.count()},
        ]
        return jsonify(stats), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
