from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.extensions import db, bcrypt  

auth_bp = Blueprint("auth", __name__)

# ------------------- Health Check -------------------
@auth_bp.route("/health")  
def health():
    return {'status': 'healthy'}, 200

# ------------------- Home/Login Page -------------------
@auth_bp.route("/", methods=["GET"], endpoint="home")
def home():
    return render_template("login.html")

# ------------------- Register Route -------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Username, email and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ------------------- Login Route -------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "يجب إدخال اسم المستخدم وكلمة المرور"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "بيانات الدخول غير صحيحة"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

# ------------------- Protected Page -------------------
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if request.accept_mimetypes.accept_html:
        return render_template("protected.html", username=user.username)
    
    return jsonify({"message": f"Access granted for user {user_id}"}), 200

# ------------------- Protected API for JS fetch -------------------
@auth_bp.route("/api/protected-data", methods=["GET"])
@jwt_required()
def protected_data():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "message": "You are viewing protected data!"
    }), 200
