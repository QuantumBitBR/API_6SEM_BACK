from flask_restx import Resource, fields, Namespace
from flask import request
from config.auth import jwt_required
from services.user_auth_service import UserAuthService, UserAlreadyExistsError


user_auth_ns = Namespace(
    'userauth', 
    description='Endpoints relacionados a autenticação de usuários')

user_auth_model = user_auth_ns.model('AuthUserModel', {
     'name': fields.String(required=True, description='Nome Completo'),
     'email': fields.String(required=True, description='Email (único)'),
     'password': fields.String(required=True, description='Senha (será hasheada)'),
     'role': fields.String(required=False, default='user', description='Perfil de acesso (ex: admin, user)')
 })

@user_auth_ns.route('/criar') 
class CriarUserAuthResource(Resource):
    @jwt_required
    @user_auth_ns.expect(user_auth_model)
    def post(self):
        """
        Registra um novo usuário de autenticação.
        """
        try:
            user_data = user_auth_ns.payload 
            
            user_auth_service = UserAuthService()
            
            results = user_auth_service.create_new_auth_user(user_data)
            
            return {'data': results}, 201 

        except UserAlreadyExistsError as uae:
            return {'error': str(uae)}, 409
        
        except ValueError as ve:
            return {'error': str(ve)}, 400
            
        except Exception as e:
            print(f"ERRO INTERNO: {e}") 
            return {'error': 'Erro interno ao registrar usuário.'}, 500