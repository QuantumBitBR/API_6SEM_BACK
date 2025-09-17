from config.db_connection import get_cursor

class CompaniesRepository:
        
    def get_companies_with_users(self):
        """
        Executa a consulta no banco de dados para obter todas as empresas com seus usuários.
        """
        sql_query = """
            SELECT 
                c.name,
                u.fullname
            FROM 
                companies c
            JOIN 
                users u ON c.companyid = u.companyid
            ORDER BY 
                c.name;
        """
        with get_cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()

            return [(str(company_name), str(user_fullname)) for company_name, user_fullname in results]