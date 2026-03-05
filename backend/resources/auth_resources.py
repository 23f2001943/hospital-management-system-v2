from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password, verify_password
from extensions import db
from models import User, Role, Doctor, Patient
from flask import current_app
import uuid
from flask import Blueprint, request, jsonify


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
    if data.get("role") == "doctor":
        return {"message": "Doctors cannot self-register"}, 403
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {"message": "Invalid input"}, 400

    if User.query.filter_by(email=email).first():
        return {"message": "User already exists"}, 400

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    # FORCE patient role
    user = datastore.create_user(
        name=name,
        email=email,
        password=hash_password(password),
        fs_uniquifier=str(uuid.uuid4()),
        active=True
    )

    patient_role = datastore.find_role("patient")
    datastore.add_role_to_user(user, patient_role)

    patient = Patient(user_id=user.id)
    db.session.add(patient)

    db.session.commit()

    return {
        "id": user.id,
        "email": user.email,
        "role": "patient"
    }, 201

