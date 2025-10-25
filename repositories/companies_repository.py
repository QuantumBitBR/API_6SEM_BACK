from config.db_connection import get_cursor, get_cursor_db_keys

class CompaniesRepository:
    def get_companies_with_users_data(self):
        """
        Busca empresas com o fullname dos usuários (criptografado)
        e adiciona a chave correspondente (do banco secundário).
        """
        with get_cursor_db_keys() as cur_keys:
            cur_keys.execute("SELECT id_user, key_encrypt FROM encrypt_user ORDER BY id_user;")
            keys = cur_keys.fetchall()

        keys_map = {row[0]: row[1] for row in keys}

        sql_query = """
            SELECT 
                c.companyid,
                c.name AS company_name,
                u.userid,
                u.fullname AS fullname_enc
            FROM companies c
            JOIN users u ON u.companyid = c.companyid
            ORDER BY c.companyid, u.userid;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            rows = cur.fetchall()

        combined_results = []
        for row in rows:
            userid = row[2]
            key_encrypt = keys_map.get(userid)
            if key_encrypt is None:
                continue  # ignora este usuário

            combined_results.append(
                (row[0], row[1], userid, row[3], key_encrypt)
            )

        return combined_results
    
    def get_all_companies(self):
        """
        Busca todas as empresas.
        """
        sql_query = "SELECT * FROM companies;"
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()