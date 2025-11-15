from flask_restx import Namespace, Resource, fields
from flask import request
from services.user_service import UserService
from models.user import user_schema
from config.auth import jwt_required

users_ns = Namespace(
    'Usuários de tickets',
    description='Endpoints relacionados a usuários dos tickets'
)

@users_ns.route("/delete")
class DeleteUser(Resource):
    @users_ns.doc(params={
        'userid': {
            'description': 'ID do usuário a ser deletado',
            'type': 'int',
            'required': True
        }
    })
    @jwt_required
    def delete(self):
        userid = request.args.get("userid", type=int)
        if userid == None:
            return {
                "error": "id cannot be null"
            }, 500
        
        user_service = UserService()
        result, status = user_service.delete_data_user(userid)
        return result, status
    
@users_ns.route('/user-by-email')
class UserByEmail(Resource):
    @jwt_required
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

    
    
