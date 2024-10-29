from flask import Blueprint, request, jsonify
from services.auth_service import signup_service, login_service
from services.token_service import refresh_token_service, is_token_revoked

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return signup_service(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_service(data)

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    is_token_revoked(refresh_token)
    if not refresh_token:
        return jsonify({"msg": "Missing refresh token"}), 400
    return refresh_token_service(refresh_token)