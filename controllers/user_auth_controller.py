from flask_restx import Resource, fields, Namespace, reqparse
from flask import request
from config.auth import jwt_required
from services.user_auth_service import UserAuthService, UserAlreadyExistsError, UserNotFoundException


user_auth_ns = Namespace(
    'userauth', 
    description='Endpoints relacionados a autenticação de usuários')

user_auth_model = user_auth_ns.model('AuthUserModel', {
     'name': fields.String(required=True, description='Nome Completo'),
     'email': fields.String(required=True, description='Email (único)'),
     'password': fields.String(required=True, description='Senha (será hasheada)'),
     'role': fields.String(required=False, default='user', description='Perfil de acesso (ex: admin, user)')
 })

delete_parser = reqparse.RequestParser()
delete_parser.add_argument(
    'user_id', 
    type=int, 
    location='args',  
    required=True, 
    help='ID do usuário a ser deletado'
)

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
        
@user_auth_ns.route('/deletar')
class DeletarUserAuthResource(Resource):
    @user_auth_ns.expect(delete_parser)
    def delete(self):
        """
        Deleta um usuário de autenticação pelo ID (passado como query parameter).
        """
        try:
            args = delete_parser.parse_args()
            user_id = args['user_id'] 

            user_auth_service = UserAuthService()
            
            user_auth_service.delete_auth_user(user_id)
            
            return {
                'message': 'Usuario deletado com sucesso', 
                'user_id': user_id
                }, 204 

        except UserNotFoundException as unf:
            return {'error': str(unf)}, 404
            
        except Exception as e:
            print(f"ERRO INTERNO: {e}") 
            return {'error': 'Erro interno ao deletar usuário.'}, 500