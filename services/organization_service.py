from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.organization import Organization
from models.user import User
from bson import ObjectId

def get_all_organizations():
    organizations = Organization.get_al_organizations()
    for org in organizations:
        org['_id'] = str(org['_id'])
    return jsonify(organizations), 200

def get_organization_by_id(organization_id):
    organization = Organization.get_organization_by_id(ObjectId(organization_id))
    if not organization:
        return jsonify({"msg": "Organization not found"}), 404
    organization['_id'] = str(organization['_id'])
    return jsonify(organization), 200

def invite_user_to_organization(organization_id, email, current_user_email):
    if not email:
        return jsonify({"msg": "Missing email"}), 400

    organization = Organization.get_organization_by_id(ObjectId(organization_id))
    if not organization:
        return jsonify({"msg": "Organization not found"}), 404

    if not any(member['email'] == current_user_email for member in organization['organization_members']):
        return jsonify({"msg": "You are not a member of the organization"}), 403

    user = User.find_by_email(email)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if any(member['email'] == email for member in organization['organization_members']):
        return jsonify({"msg": "User already a member"}), 400

    organization['organization_members'].append({
        "name": user['name'],
        "email": user['email'],
        "access_level": "member"
    })
    Organization.update_organization_members(ObjectId(organization_id), organization['organization_members'])

    return jsonify({"msg": "User invited successfully"}), 200

def create_organization(data):
    name = data.get('name')
    description = data.get('description')
    organization_id = Organization.create_organization(name, description, User.find_by_email(get_jwt_identity()))
    return jsonify({"organization_id": organization_id}), 200

def delete_organization(organization_id, current_user_email):
    current_user = User.find_by_email(current_user_email)
    if not current_user:
        return jsonify({"msg": "User not found"}), 404

    Organization.delete_organization(ObjectId(organization_id))
    return jsonify({"msg": "Organization deleted successfully"}), 200

def update_organization(organization_id, data):
    organization = Organization.get_organization_by_id(ObjectId(organization_id))
    if not organization:
        return jsonify({"msg": "Organization not found"}), 404

    organization['name'] = data.get('name', organization['name'])
    organization['description'] = data.get('description', organization['description'])
    Organization.update_organization(ObjectId(organization_id), organization)

    return jsonify({"msg": "Organization updated successfully"}), 200