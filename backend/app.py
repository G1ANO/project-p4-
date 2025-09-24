from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db, ma, bcrypt, User, Plan, Subscription
from marshmallow import validates, ValidationError, fields


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


user_schema = UserSchema()
users_schema = UserSchema(many=True)
plan_schema = PlanSchema()
plans_schema = PlanSchema(many=True)
subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)



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
        if Plan.query.count() == 0:
            basic = Plan(name="Basic", price=5.0, duration_minutes=60)
            premium = Plan(name="Premium", price=15.0, duration_minutes=300)
            db.session.add_all([basic, premium])
            db.session.commit()

   

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
    
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"message": "Flask backend is running 🚀"}), 200
 

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data.get("email")).first()

        if user and bcrypt.check_password_hash(user.password_hash, data.get("password")):
            return user_schema.jsonify(user), 200
        return jsonify({"error": "Invalid email or password"}), 401

    @app.route("/users", methods=["GET"])
    def get_users():
        users = User.query.all()
        return users_schema.jsonify(users), 200

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return user_schema.jsonify(user), 200

    @app.route("/users/<int:user_id>", methods=["PATCH"])
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]

        db.session.commit()
        return user_schema.jsonify(user), 200

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200

    @app.route("/plans", methods=["GET"])
    def get_plans():
        plans = Plan.query.all()
        return plans_schema.jsonify(plans), 200
    
    @app.route("/subscriptions", methods=["GET"])
    def get_all_subscriptions():
        subs = Subscription.query.all()
        return subscriptions_schema.jsonify(subs), 200

    @app.route("/subscriptions", methods=["POST"])
    def create_subscription():
        data = request.get_json()
        user = User.query.get(data.get("user_id"))
        plan = Plan.query.get(data.get("plan_id"))

        if not user or not plan:
            return jsonify({"error": "Invalid user or plan"}), 400

        sub = Subscription(user_id=user.id, plan_id=plan.id, status="active")
        db.session.add(sub)
        db.session.commit()

        return subscription_schema.jsonify(sub), 201

    
    @app.route("/subscriptions/<int:user_id>", methods=["GET"])
    def get_user_subscriptions(user_id):
        subs = Subscription.query.filter_by(user_id=user_id).all()
        return subscriptions_schema.jsonify(subs), 200

    
    @app.route("/subscriptions/<int:sub_id>", methods=["DELETE"])
    def cancel_subscription(sub_id):
        sub = Subscription.query.get(sub_id)
        if not sub:
            return jsonify({"error": "Subscription not found"}), 404

        db.session.delete(sub)
        db.session.commit()
        return jsonify({"message": "Subscription cancelled"}), 200



    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
