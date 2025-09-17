import jwt
import datetime
from flask import request, jsonify
from functools import wraps
from os import environ

SECRET_KEY = environ.get('JWT_SECRET', 'dev_secret_key')

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def auth():
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    if user_id:
        token = generate_token(user_id)
        return jsonify({'token': token})
    return jsonify({'error': 'Credenciais inválidas'}), 401

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return {'error': 'Token ausente'}, 401
        data = decode_token(token)
        if not data:
            return {'error': 'Token inválido ou expirado'}, 401
        return f(*args, **kwargs)
    return decorated