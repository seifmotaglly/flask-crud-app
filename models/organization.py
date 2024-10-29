from flask import current_app
from flask_jwt_extended import get_jwt_identity

class Organization:
    
    @staticmethod
    def create_organization(name, description, current_user):
        organization = {
        'name': name,
        'description' : description,
        'organization_members':[
            {
                "name": current_user['name'],
                "email": current_user['email'],
                "access_level": "admin"
            }
        ]
        }
        organization_id = current_app.config['MONGO_DB'].organizations.insert_one(organization).inserted_id
        return str(organization_id)
    
    @staticmethod
    def get_al_organizations():
        organizations = list(current_app.config['MONGO_DB'].organizations.find())
        return organizations
    
    @staticmethod
    def get_organization_by_id(organization_id):
        organization = current_app.config['MONGO_DB'].organizations.find_one({"_id": organization_id})
        return organization
    
    @staticmethod
    def update_organization_members(organization_id, members):
        current_app.config['MONGO_DB'].organizations.update_one({"_id": organization_id}, {"$set": {"organization_members": members}})
        
    @staticmethod
    def delete_organization(organization_id):
        current_app.config['MONGO_DB'].organizations.delete_one({"_id": organization_id})
        
    @staticmethod
    def update_organization(organization_id, organization):
        current_app.config['MONGO_DB'].organizations.update_one(
            {"_id": organization_id},
            {"$set": {"name": organization['name'], "description": organization['description']}}
        )