from config.db_connection import get_cursor
from repositories.privacy_policy_repository import PrivacyPolicyRepository
from services.user_service import UserService

class PrivacyPolicyService:
    def __init__(self):
        self.privacy_repository = PrivacyPolicyRepository()
        self.user_service = UserService()
    
    def get_privacy_policies(self,):
        try:
            response = self.privacy_repository.get_privacy_policies()
            return {"data": [{"id": id, "text": text,"validity_date": validity_date.strftime("%d/%m/%Y %H:%M:%S") if validity_date else None, "is_mandatory": is_mandatory if is_mandatory != None else False} for id, text, validity_date, is_mandatory in response]}, 200
        except Exception:
            return {
                "error": "Algo ocorreu errado"
            }, 500
        
    def get_all_privacy_by_user(self, userid: int):
        try:
            user = self.user_service.get_user_authentication_by_id(userid)
            if user[1] == 404:
                return user
            response = self.privacy_repository.get_all_privacy_by_user(userid)
            return {"data": [{"id": id, "text": text,"validity_date": validity_date.strftime("%d/%m/%Y %H:%M:%S") if validity_date else None, "is_mandatory": is_mandatory if is_mandatory != None else False,"is_accept": not is_revoke if is_revoke != None else False} for id, text, validity_date, is_mandatory, is_revoke in response]}, 200
        except Exception as e:

            return {
                "error": "Algo ocorreu errado"
            }, 500
        
    def add_accept_privacy(self, userid, privacy_id):
        try:
            response = self.privacy_repository.get_accept(userid, privacy_id)
            try:
                response = response[0]
            except Exception:
                response = None

            if response == None: 
                response = self.privacy_repository.post_new_accept(userid, privacy_id)
                if response:
                    log = self.privacy_repository.add_log_privacy(userid, privacy_id, "Termo de privacidade aceito")
                    if not log:
                        return {"error": "Algo ocorreu errado"}, 500 
                    return {"message": "Termo de privacidade aceito com sucesso!"}, 201
                
                return {"error": "Algo ocorreu errado"}, 500
            
            is_revoke = not response
            result = self.privacy_repository.revoke_reaccept_policy(userid, privacy_id, is_revoke)
            
            if result and is_revoke:
                log = self.privacy_repository.add_log_privacy(userid, privacy_id, "Termo de privacidade revogado")
                if not log:
                    return {"error": "Algo ocorreu errado"}, 500 
                return {"message": "Termo de privacidade revogado!"}, 201

            if result and not is_revoke:
                log = self.privacy_repository.add_log_privacy(userid, privacy_id, "Termo de privacidade aceito")
                if not log:
                    return {"error": "Algo ocorreu errado"}, 500 
                return {"message": "Termo de privacidade aceito com sucesso!"}, 201
            
            return {"error": "Algo ocorreu errado"}, 500
        except Exception:
            return {"error": "Algo ocorreu errado"}, 500
        
    def get_current_privacy(self):
        return self.privacy_repository.get_current_privacy()

    def get_last_user_accept(self, userid):
        return self.privacy_repository.get_last_user_accept(userid)
    
    def get_last_policy_user_accept(self, userid, privacy_id):
        return self.privacy_repository.get_last_user_accept(userid, privacy_id)
    
    def create_privacy_policy(self, text: str, is_mandatory: bool):
        response = self.privacy_repository.create_privacy_policy(text, is_mandatory)
        if response:
            return {"message": "Criado com sucesso"}, 201
        
        return {"error": "Algo ocorreu errado"}, 500
    def get_is_assigned_unmandatory_policy(self, userid: int):
        try:
            response = self.privacy_repository.get_privacy_unmandatory_privacy_by_user(userid)
            return {"data": {
                        "is_accept": response
                    }
                }, 200
        except Exception:
            return {
                "error": "Algo ocorreu errado"
            }, 500
    