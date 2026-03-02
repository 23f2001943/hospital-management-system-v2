from flask import Blueprint, jsonify
from flask_security.decorators import auth_required, roles_required
from models import User
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/approve-doctor/<int:user_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("admin")
def approve_doctor(user_id):
    user = User.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    if not any(role.name == "doctor" for role in user.roles):
        return {"message": "User is not a doctor"}, 400

    user.active = True
    db.session.commit()

    return jsonify({
        "message": "Doctor approved successfully",
        "doctor_id": user.id,
        "active": user.active
    })