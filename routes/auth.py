from flask import Blueprint, request, jsonify
from services.auth_service import signup_service, login_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return signup_service(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_service(data)