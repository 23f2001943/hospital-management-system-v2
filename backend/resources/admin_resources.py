from flask import Blueprint, request, jsonify
from flask_security import auth_required
from flask_security.decorators import roles_required
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from extensions import db
from models import User, Role, Doctor
import uuid

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/add-doctor", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def add_doctor():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    department_id = data.get("department_id")

    if not name or not email or not password or not department_id:
        return {"message": "Missing fields"}, 400

    if User.query.filter_by(email=email).first():
        return {"message": "Doctor already exists"}, 400

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    user = datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        active=True
    )

    doctor_role = datastore.find_role("doctor")
    datastore.add_role_to_user(user, doctor_role)

    doctor = Doctor(
        user_id=user.id,
        specialization_id=department_id
    )
    db.session.add(doctor)
    db.session.commit()

    return jsonify({
        "message": "Doctor added successfully",
        "doctor_id": user.id
    }), 201