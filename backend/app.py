# backend/app.py
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User, Plan, Subscription

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)
CORS(app)

# ✅ Home route
@app.route("/")
def home():
    return jsonify({"message": "Backend running!"})

# ✅ Register user
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    new_user = User(username=data["username"], email=data["email"], password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 🔹 Creates tables if not exist
    app.run(debug=True)
