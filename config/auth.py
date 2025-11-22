import jwt
import datetime
from flask import request
from functools import wraps
from os import environ
from werkzeug.security import check_password_hash
from services.user_service import UserService
from services.privacy_policy_service import PrivacyPolicyService

def generate_token(user):
    """Gera JWT para o usuário"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'name': user.name,
        'exp': int((datetime.datetime.utcnow() + datetime.timedelta(hours=12)).timestamp())
    }
    token = jwt.encode(payload, environ.get("SECRET_KEY"), algorithm="HS256")
    return token


def decode_token(token):
    """Decodifica JWT"""
    try:
        return jwt.decode(token, environ.get("SECRET_KEY"), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_policy_terms(user_id):
    """
    Verifica se o usuário aceitou a última versão da política.
    Retorna um dicionário com o status.
    """
    privacy_service = PrivacyPolicyService()
    current_policy = privacy_service.get_current_privacy()
    if(current_policy):

        last_policy = privacy_service.get_last_user_accept(user_id, current_policy[0])
    policy_expired = True
    if last_policy and current_policy:
        policy_expired = current_policy[0] != last_policy[1]

    return {
        'policy_expired': policy_expired,
        'current_policy': {
            'id_policy': current_policy[0] if current_policy else None,
            'text_policy': current_policy[1] if current_policy else None,
            'policy_date': current_policy[2].isoformat() if current_policy else None,
            'is_mandatory': current_policy[3] if current_policy else False,

        }
    }


def auth():
    """Autenticação via Basic Auth"""
    data = request.authorization

    if not data or not data.username or not data.password:
        return {'error': 'Credenciais inválidas'}, 401

    # Pega usuário pelo email
    user_service = UserService()
    user = user_service.user_by_email(data.username).first()

    if not user:
        return {'error': 'Usuário não encontrado'}, 401

    # Verifica senha
    if check_password_hash(user.password, data.password):
        token = generate_token(user)
        # usa check_policy_terms separado
        policy_info = check_policy_terms(user.id)
        privacy_police_service = PrivacyPolicyService()
        response = privacy_police_service.get_is_assigned_unmandatory_policy(user.id)
        
        if response[1] == 200:
            return {
                'user_id': user.id,
                'role': user.role,
                'token': token,
                **policy_info,   # junta os dados de política no retorno
                'is_accept_unmandatory': response[0]['data']['is_accept']
            }, 200
        else:
            return {'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}, 401

    return {'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}, 401


def jwt_required(f):
    """Decorator para rotas protegidas com JWT"""
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

        # só valida e segue, sem passar argumento extra
        return f(*args, **kwargs)
    return decorated

