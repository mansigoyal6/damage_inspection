from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .models import create_user, get_user_by_username

auth_bp = Blueprint('auth', __name__, url_prefix='/')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    user_id = create_user(username, password)
    if not user_id:
        return jsonify({'error': 'Username already exists'}), 409
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = get_user_by_username(username)
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200