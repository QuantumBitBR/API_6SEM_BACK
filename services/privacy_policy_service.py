from config.db_connection import get_cursor
from repositories.privacy_policy_repository import PrivacyPolicyRepository

class PrivacyPolicyService:
    def __init__(self):
        self.privacy_repository = PrivacyPolicyRepository()
        
    def add_accept_privacy(self, userid, privacy_id):
        response = self.privacy_repository.post_new_accept(userid, privacy_id)
        return response
        
    def get_current_privacy(self):
        return self.privacy_repository.get_current_privacy()

    def get_last_user_accept(self, userid):
        return self.privacy_repository.get_last_user_accept(userid)
    
    def get_last_policy_user_accept(self, userid, privacy_id):
        return self.privacy_repository.get_last_user_accept(userid, privacy_id)