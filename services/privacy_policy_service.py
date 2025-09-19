from config.db_connection import get_cursor
from repositories.privacy_policy_repository import PrivacyPolicyRepository

class PrivacyPolicyService:
    def __init__(self):
        self.privacy_repository = PrivacyPolicyRepository()
        
    def add_accept_privacy(self, userid, privacy_id):
        response = self.privacy_repository.post_new_accept(userid, privacy_id)
        return response
        