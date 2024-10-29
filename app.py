import time
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, get_jwt, jwt_required
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

max_retries = 5
for i in range(max_retries):
    try:
        mongo = PyMongo(app)
        app.config['MONGO_DB'] = mongo.db
        break
    except Exception as e:
        if i < max_retries - 1:
            time.sleep(5)
        else:
            raise e

jwt = JWTManager(app)

from routes.auth import auth_bp
from routes.protected import protected_bp

app.register_blueprint(auth_bp)
app.register_blueprint(protected_bp)

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)