from flask import Blueprint, request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user
from .extensions import db
from .models import *



auth_bp = Blueprint("auth", __name__)

#Register

@auth_bp.route("/register",methods=["POST"])
def register():
    data = request.json
    hashed_pwd = generate_password_hash(data["password"])

    user = User(
        email = data["email"],
        password = hashed_pwd
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User Registerd"})



@auth_bp.route("/users", methods=["GET"])
def get_user_list():
    users = User.query.all()
    result=[
        {
            "id":u.id,
            "email":u.email,
        }
        for u in users
    ]
    return jsonify(result),200

@auth_bp.route("/user_by_id/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not found"}), 404
    

    print(user,'user----')

    result = [
        {
            "id":user.id,
            "email":user.email,
            "password":user.password,
            "role":user.role,
        }
        
    ]
    return jsonify(result),200



@auth_bp.route("/update_user/<int:id>",methods=["PUT"])
def update_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error": "User not fount"}),404
    
    data = request.json

    email = data.get("email")
    role = data.get("role")

    user.email = email,
    user.role = role

    db.session.commit()

    return jsonify({"message":"User detail updated Successfully"})


@auth_bp.route("delete_users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200


@auth_bp.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@auth_bp.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Something went wrong"}), 500



#Login
@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email= data["email"]).first()

    if user and check_password_hash(user.password,data["password"]):
        login_user(user)
        return jsonify({"message": "Login Success"})
    
    return jsonify({"message": "Invalid credentials"}),401

#Logout

@auth_bp.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})



# ====================== 19-01-2025 ===============================================

import logging

logging.basicConfig(
    filename="auth_routes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("User API called")

logging.warning("Invalid user id")

logging.error("Database connection failed")


# Error handling ensures application stability by gracefully managing failures, 
# while logging helps track and debug issues by recording system events and errors.

@auth_bp.route("/get_user_id/<int:id>")
def get_user_id(id):
    try:
        user=User.query.get(id)

        if not user:
            logging.warning(f"User not found {id}")
            return jsonify({"error":"User not found"}),404

        return jsonify({"id":user.id,"email":user.email}) 
    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "Internal server error"}),500













