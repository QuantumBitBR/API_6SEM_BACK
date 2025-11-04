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

model_privacy_policy_create = privacy_policy_ns.model('PrivacyCreate', {
    'text': fields.String(required=True, description='Privacy policy description/text'),
    'is_mandatory': fields.Boolean(required=True, description='Define if the privacy is mandatory or not.')
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
            },500
        policy_service = PrivacyPolicyService()

        response = policy_service.add_accept_privacy(id_user, id_privacy)

        return response
    
@privacy_policy_ns.route("/create")
class CreatePrivacy(Resource):
    @privacy_policy_ns.expect(model_privacy_policy_create, validate=True)
    def post(self):
        request_body = request.get_json()
        text = request_body.get('text') if request_body else None
        is_mandatory = request_body.get('is_mandatory') if request_body else None

        if text == None or is_mandatory == None:
            return {
                "error": "text and is_mandatory cannot be null or empty"
            }, 500
        
        service = PrivacyPolicyService()

        response = service.create_privacy_policy(text, is_mandatory)

        return response
