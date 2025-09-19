from config.db_connection import get_cursor
from datetime import datetime

class PrivacyPolicyRepository:
    def __init__(self):
        pass

    def post_new_accept(self, userid: int, privacypolicyid: int):
        sql_query = """
            INSERT INTO privacy_policy_version_accept (id_user, id_privacy_policy, validity_date)
            VALUES (%s, %s, %s)
        """
        try:
            with get_cursor() as cur:
                cur.execute(sql_query, (userid, privacypolicyid, datetime.now()))
                return True
        except Exception as e:
            return False
        
    def get_current_privacy(self):
        sql_query = """
            SELECT * FROM privacy_policy_version order by validity_date DESC limit 1;
        """
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchone()