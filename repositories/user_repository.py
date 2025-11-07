from config.db_connection import get_cursor, get_cursor_db_keys

class UserRepository:
    def __init__(self):
        pass

    def delete_data_user(self, userid: int):
        first_sql_query = """
            DELETE FROM encrypt_user WHERE id_user = %s
        """
        second_sql_query = """
            SELECT ticketid FROM tickets WHERE createdbyuserid = %s
        """

        third_sql_query = """
            DELETE FROM encrypt_ticket WHERE ticketid IN %s
        """
        ticket_ids = ()

        with get_cursor() as cur:
            cur.execute(second_sql_query, (userid, ))
            rows = cur.fetchall()
            ticket_ids = tuple(row[0] for row in rows)


        with get_cursor_db_keys() as cur:
            try: 
                if ticket_ids:
                    cur.execute(third_sql_query, (ticket_ids, ))

                cur.execute(first_sql_query, (userid, ))
                return True
            except Exception as e:
                return False

    def get_by_id(self, userid):
        sql_query = """
            SELECT * FROM users where userid = %s
        """

        with get_cursor() as cur:
            cur.execute(sql_query, (userid,))
            row = cur.fetchone()
            if row:
                return row             
                    
            return None
        
    def get_user_authentication_by_id(self, userid):
        sql_query = """
            SELECT * FROM user_authentication where id = %s
        """

        with get_cursor() as cur:
            cur.execute(sql_query, (userid,))
            row = cur.fetchone()
            if row:
                return {
                    "id": row[0], 
                    "name": row[1],
                    "role":row[2],
                    "email":row[3],
                    "password":row[4],
                    "createdat": row[5].isoformat() if row[5] else None
                }
            return None
        
    
             