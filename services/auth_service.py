from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import User

def signup_service(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({"msg": "Missing name, email, or password"}), 400

    user = User.find_by_email(email)
    if user:
        return jsonify({"msg": "User already exists"}), 400

    User.create_user(name, email, password)
    return jsonify({"msg": "User registered successfully"}), 201

def login_service(data):
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.find_by_email(email)
    if not user or not User.check_password(user,password):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200