import jwt
import datetime
from os import environ
from functools import wraps
from flask import request, jsonify

secret_key = environ.get('SECRET_KEY')


def create_access_token(user_id, isAdmin=False):
    """
     Function to decode the payload
    """
    payload = {
        "uid": user_id,
        "adm": isAdmin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")
    return token


def decoded_token(token):
    """ 
    Function to decode the the token 
    """
    decoded = jwt.decode(token, secret_key, algorithms="HS256")
    return decoded


def extract_token_from_header():
    """
    Get token fromm the headers
    """
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or "Bearer" not in authorization_header:
        return jsonify({
            "error": "Bad authorization header",
            "status": 400
        })
    token = authorization_header.split(" ")[1]
    return token


def jwt_required(function):
    """
    Only requests with Authorization headers required
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        response = None
        try:
            extract_token_from_header()
            response = function(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = jsonify({
                "error": "Your token has expired",
                "status": 401
            }), 401
        except jwt.InvalidTokenError:
            response = jsonify({
                "error": "Invalid token",
                "status": 401
            }), 401
        return response
    return wrapper


def get_identity():
    """
    Retrieve user_id from the token
    """
    return decoded_token(extract_token_from_header())["uid"]


def verify_is_admin():
    """Get user_role from the token"""
    return decoded_token(extract_token_from_header())["adm"]


def admin_denied(function):
    """
    Admin denied
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if verify_is_admin():  
            return jsonify({
                "error": "Admin denied",
                "status": 403
            }), 403
        return function(*args, **kwargs)
    return wrapper


def admin_required(function):
    """
    Deny non admin from accessing the resource
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not verify_is_admin():
            return jsonify({
                "error": "Only Admins can access this resource",
                "status": 403
            }), 403
        return function(*args, **kwargs)
    return wrapper


def json_data_required(function):
    """
    Only requests with Content-type json will be allowed
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                "status": 400,
                "error": "JSON data required"
            }), 400
        return function(*args, **kwargs)
    return wrapper