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






















