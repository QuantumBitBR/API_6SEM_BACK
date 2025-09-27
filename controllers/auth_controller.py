import config.auth as auth
from flask_restx import Namespace, Resource

auth_ns = Namespace(
    'auth', 
    description='Endpoints de autenticação com JWT'
)

@auth_ns.route('/login')
class AuthResource(Resource):
    def post(self):
        return auth.auth()
