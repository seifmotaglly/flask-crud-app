from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from services.organization_service import (
    get_all_organizations,
    get_organization_by_id,
    invite_user_to_organization,
    create_organization,
    delete_organization,
    update_organization
)
from services.token_service import revoke_refresh_token_service, is_token_revoked

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/organization', methods=['GET'])
@jwt_required()
def get_organizations():
    is_token_revoked(get_jwt())
    return get_all_organizations()

@protected_bp.route('/organization/<organization_id>', methods=['GET'])
@jwt_required()
def get_organization(organization_id):
    is_token_revoked(get_jwt())
    return get_organization_by_id(organization_id)

@protected_bp.route('/organization/<organization_id>/invite', methods=['POST'])
@jwt_required()
def invite_member(organization_id):
    email = request.get_json().get('email')
    current_user_email = get_jwt_identity()
    is_token_revoked(get_jwt())
    return invite_user_to_organization(organization_id, email, current_user_email)

@protected_bp.route('/organization', methods=['POST'])
@jwt_required()
def create_org():
    data = request.get_json()
    is_token_revoked(get_jwt())
    return create_organization(data)

@protected_bp.route('/organization/<organization_id>', methods=['DELETE'])
@jwt_required()
def delete_org(organization_id):
    is_token_revoked(get_jwt())
    current_user_email = get_jwt_identity()
    return delete_organization(organization_id, current_user_email)

@protected_bp.route('/organization/<organization_id>', methods=['PUT'])
@jwt_required()
def update_org(organization_id):
    data = request.get_json()
    is_token_revoked(get_jwt())
    return update_organization(organization_id, data)

@protected_bp.route('/revoke-refresh-token', methods=['POST'])
@jwt_required()
def revoke_refresh():
    refresh_token = request.json.get('refresh_token')
    is_token_revoked(refresh_token)
    if not refresh_token:
        return jsonify({"msg": "Missing refresh token"}), 400
    return revoke_refresh_token_service(refresh_token)