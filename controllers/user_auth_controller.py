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

user_update_model = user_auth_ns.model('UserUpdateModel', {
     'name': fields.String(required=False, description='Nome Completo'),
     'role': fields.String(required=False, description='Perfil de acesso')
})

id_parser = reqparse.RequestParser()
id_parser.add_argument(
    'user_id', 
    type=int, 
    location='args',  
    required=True, 
    help='ID do usuário na Query String (?user_id=X)'
)

id_parser = reqparse.RequestParser()
id_parser.add_argument(
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
    @jwt_required
    @user_auth_ns.expect(id_parser)
    def delete(self):
        """
        Deleta um usuário de autenticação pelo ID (passado como query parameter).
        """
        try:
            args = id_parser.parse_args()
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

@user_auth_ns.route('/atualizar') 
class UpdateUserAuthResource(Resource):
    @user_auth_ns.expect(user_update_model)
    @user_auth_ns.expect(id_parser)
    def put(self):
        """
        Atualiza os dados de um usuário de autenticação pelo ID.
        """
        try:

            id_args = id_parser.parse_args()
            user_id = id_args['user_id']
            
            user_data = user_auth_ns.payload 
            
            if not user_data:
                 return {'error': 'Nenhum dado fornecido para atualização.'}, 400
        
            if any(field in user_data for field in ['email', 'password']):
                return {'error': 'A edição de email e senha não é permitida neste endpoint.'}, 403

            user_auth_service = UserAuthService()
            results = user_auth_service.update_auth_user(user_id, user_data)

            return {'data': results}, 200

        except UserNotFoundException as unf:
            return {'error': str(unf)}, 404
            
        except Exception as e:
            print(f"ERRO INTERNO: {e}") 
            return {'error': 'Erro interno ao atualizar usuário.'}, 500
        
@user_auth_ns.route("/by_id")
class UserAuthenticationById(Resource):
   
    @user_auth_ns.expect(id_parser)
    def get(self):
        args = id_parser.parse_args()
        user_id = args['user_id']
        user_service = UserAuthService()
        result, status = user_service.get_user_authentication_by_id(user_id)
        return result, status
    