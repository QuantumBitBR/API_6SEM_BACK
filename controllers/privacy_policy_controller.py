from services.privacy_policy_service import PrivacyPolicyService
from flask_restx import Namespace, Resource, fields
from flask import request


privacy_policy_ns = Namespace(
    'Privacy Policy', 
    description='Endpoints ao termo de privacidade'
)

model_privacy_policy_accept = privacy_policy_ns.model('PrivacyAcceptPost', {
    'userid': fields.Integer(required=True, description='User id'),
    'privacyid': fields.Integer(required=True, description='Privacy police version id')
})

@privacy_policy_ns.route("/accept")
class AcceptPrivacy(Resource):
    @privacy_policy_ns.expect(model_privacy_policy_accept, validate=True)
    def post(self):
        request_body = request.get_json()
        id_user = request_body.get('userid') if request_body else None 
        id_privacy = request_body.get('privacyid') if request_body else None 

        if id_user == None or id_privacy == None:
            return{
                "error": "privacyid and userid cannot be null or empty"
            }
        policy_service = PrivacyPolicyService()

        if policy_service.add_accept_privacy(id_user, id_privacy):
            return {}, 201
        return {
            "error": "Something is wrong"
        }, 500