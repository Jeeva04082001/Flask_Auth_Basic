from flask import Blueprint, jsonify
from flask_login import login_required, current_user


protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/dashboard")
@login_required
def dashboard():
    return "Welcom User"



@protected_bp.route("/admin")
@login_required
def admin():
    print("ROLE:", current_user.role)
    if current_user.role != "admin":
        return jsonify({"error": "Access Denied"}),403
    return "Welcome Admin"

















