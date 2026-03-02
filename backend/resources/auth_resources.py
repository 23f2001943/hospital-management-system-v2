from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from extensions import db
from models import User, Role, Doctor, Patient
from flask import current_app
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash as verify_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(password, user.password):
        return jsonify({'message': 'Invalid email or password'}), 400

    roles = [role.name for role in user.roles]

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "roles": roles,
        "token": user.get_auth_token()
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role_name = data.get("role")

    if not name or not email or not password or role_name not in ["doctor", "patient"]:
        return {"message": "Invalid input"}, 400

    if User.query.filter_by(email=email).first():
        return {"message": "User already exists"}, 400

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    #doctor approval logic
    active = True
    if role_name == "doctor":
        active = False   # doctor needs admin approval

    # create user
    user = datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        active=active
    )

    role = datastore.find_role(role_name)
    datastore.add_role_to_user(user, role)

    db.session.flush()  # get user.id

    # role-specific table
    if role_name == "doctor":
        department_id = data.get("department_id")
        if not department_id:
            return {"message": "department_id required for doctor"}, 400

        doctor = Doctor(
            user_id=user.id,
            specialization_id=department_id
        )
        db.session.add(doctor)

    elif role_name == "patient":
        patient = Patient(
            user_id=user.id
        )
        db.session.add(patient)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500

    return {
        "id": user.id,
        "email": user.email,
        "role": role_name,
        "active": active
    }, 201