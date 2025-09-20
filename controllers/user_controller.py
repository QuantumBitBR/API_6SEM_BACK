from flask_restx import Namespace, Resource, fields
from flask import request
from services.user_service import UserService

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
    def delete(self):
        userid = request.args.get("userid", type=int)
        if userid == None:
            return {
                "error": "id cannot be null"
            }, 500
        
        user_service = UserService()
        result, status = user_service.delete_data_user(userid)
        return result, status