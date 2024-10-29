from flask import jsonify
from flask_jwt_extended import decode_token, create_access_token, create_refresh_token
from extensions import redis_client

def refresh_token_service(refresh_token):
    if(is_token_revoked(refresh_token)):
        return jsonify({"msg": "Token has already been revoked"}), 400
    
    try:
        decoded_token = decode_token(refresh_token)
        current_user = decoded_token['sub']
        new_access_token = create_access_token(identity=current_user)
        new_refresh_token = create_refresh_token(identity=current_user)
        return jsonify(msg="tokens refreshed", new_refresh_token=new_refresh_token, access_token=new_access_token), 200
    except Exception as e:
        return jsonify({"msg": "Invalid refresh token"}), 401

def revoke_refresh_token_service(refresh_token):
    if(is_token_revoked(refresh_token)):
        return jsonify({"msg": "Token has already been revoked"}), 400
    
    try:
        decoded_token = decode_token(refresh_token)
        jti = decoded_token["jti"]
        redis_client.set(jti, "revoked", ex=3600) 
        return jsonify({"msg": "Refresh token successfully revoked"}), 200
    except Exception as e:
        return jsonify({"msg": "Invalid refresh token"}), 401

def is_token_revoked(token):
    try:
        jti = decode_token(token)["jti"]
        token_in_redis = redis_client.get(jti)
        return token_in_redis is not None
    except Exception as e:
        return True