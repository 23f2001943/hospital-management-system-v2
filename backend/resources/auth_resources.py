from flask import Blueprint, jsonify, request
from flask_security.utils import verify_password
from models import User

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