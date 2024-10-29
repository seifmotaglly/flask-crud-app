from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

class User:
    
    @staticmethod
    def find_by_email(email):
        return current_app.config['MONGO_DB'].users.find_one({"email": email})

    @staticmethod
    def create_user(name, email, password):
        hashed_password = generate_password_hash(password)
        current_app.config['MONGO_DB'].users.insert_one({"name": name, "email": email, "password": hashed_password})

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user['password'], password)