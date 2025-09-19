from flask_restx import Namespace, Resource
from flask import request
from services.user_service import UserService
from config.auth import jwt_required
from models.user import user_schema

user_ns = Namespace(
    'User', 
    description='Endpoints relacionados a usuários'
)

@user_ns.route('/user-by-email')
class UserByEmail(Resource):
    def get(self):
        """
        Busca usuário por email.
        """
        try:
            data = request.get_json()
            email = data.get('email')
            user_service = UserService()
            user = user_service.user_by_email(email).first()
            
            if user:
                return {'data': user_schema.dump(user)}, 200
            else:
                return {'message': 'User not found'}, 404

        except Exception as e:
            return {'error': str(e)}, 500