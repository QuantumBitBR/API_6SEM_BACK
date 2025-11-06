from config.db_connection import get_cursor
from datetime import datetime

class PrivacyPolicyRepository:
    def __init__(self):
        pass

    def create_privacy_policy(self, text: str, is_mandatory: bool):
        sql_query = """
            INSERT INTO privacy_policy_version (text, is_mandatory, validity_date)
            VALUES (%s, %s, %s)    
        """
        try:
            with get_cursor() as cur:
                cur.execute(sql_query, (text, is_mandatory, datetime.now()))
                return True
        except Exception:
            return False

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
        
    def get_accept(self, userid: int, privacypolicyid: int):
        sql_query = """SELECT is_revoke FROM privacy_policy_version_accept where id_user = %s and id_privacy_policy = %s"""

        try:
            with get_cursor() as cur:
                cur.execute(sql_query, (userid, privacypolicyid))
                return cur.fetchone()
        except Exception:
            raise {"error": "Algo ocorreu errado"}
        
    def revoke_reaccept_policy(self, userid: int, privacypolicyid: int, is_revoke: bool):
        sql_query = """
                UPDATE privacy_policy_version_accept 
                SET is_revoke = %s, validity_date = %s where id_user = %s
                and id_privacy_policy = %s
                """
        try:
            with get_cursor() as cur:
                cur.execute(sql_query, (is_revoke, datetime.now(), userid, privacypolicyid))
                return True
        except Exception:
            return False
        
    def get_current_privacy(self):
        sql_query = """
            SELECT * FROM privacy_policy_version order by validity_date DESC limit 1;
        """
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchone()
        
    def get_last_user_accept(self, userid):
        sql_query = """
            SELECT * FROM privacy_policy_version_accept 
            WHERE id_user = %s 
            ORDER BY validity_date DESC 
            LIMIT 1;
        """
        with get_cursor() as cur:
            cur.execute(sql_query, (userid,))
            return cur.fetchone()
        
    def get_last_policy_user_accept(self, userid, privacy_id):
        sql_query = """
            SELECT * FROM privacy_policy_version_accept 
            WHERE id_user = %s AND id_privacy_policy = %s
            ORDER BY validity_date DESC 
            LIMIT 1;
        """
        with get_cursor() as cur:
            cur.execute(sql_query, (userid, privacy_id))
            return cur.fetchone()
        
    def add_log_privacy(self, userid: int, privacyid: int, description: str):
        sql_query = """INSERT INTO log_privacy_policy_accept_revoke(user_id, privacy_id, action_date,
            action_description) VALUES(%s, %s, %s, %s)"""
        
        try:
            with get_cursor() as cur:
                cur.execute(sql_query, (userid, privacyid, datetime.now(), description))
                return True
        except Exception as error:
            return False
        
    def get_privacy_policies(self):
        sql_query = """
            SELECT id, text, validity_date, is_mandatory
            FROM privacy_policy_version
            ORDER BY validity_date
        """
        try:
            with get_cursor() as cur:
                cur.execute(sql_query)
                response = cur.fetchall()
                return response
        except Exception:
            raise TypeError("Erro ao tentar buscar os  dados")

    def get_all_privacy_by_user(self, userid:int):
        sql_query = """
            SELECT p.id, p.text, p.validity_date, p.is_mandatory, u.is_revoke
            FROM privacy_policy_version p LEFT JOIN 
            privacy_policy_version_accept u on p.id = u.id_privacy_policy AND u.id_user = %s
            ORDER BY p.validity_date
        """

        try:
            with get_cursor() as cur:
                cur.execute(sql_query, (userid,))
                response = cur.fetchall()
                return response
        except Exception as e:
            raise TypeError("Erro ao tentar buscar os  dados")
