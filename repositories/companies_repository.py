from config.db_connection import get_cursor

class CompaniesRepository:
    def get_companies_with_users_data(self):
        """
        Busca empresas com o fullname dos usuários (criptografado).
        """
        sql_query = """
            SELECT 
                c.companyid,
                c.name AS company_name,
                u.userid,
                u.fullname,
                eu.key_encrypt
            FROM companies c
            JOIN users u ON u.companyid = c.companyid
            JOIN encrypt_user eu ON eu.id_user = u.userid
            ORDER BY c.companyid, u.userid;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
    
    def get_all_companies(self):
        """
        Busca todas as empresas.
        """
        sql_query = "SELECT * FROM companies;"
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()