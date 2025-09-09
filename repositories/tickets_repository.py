from config.db_connection import get_cursor

class TicketsByCompanyRepository:
    def get_tickets_by_company(self):
        """
        Executa a consulta no banco de dados para contar os tickets por empresa.
        Retorna uma lista de tuplas.
        """
        sql_query = """
            SELECT 
                c.name,
                COUNT(t.ticketid) AS ticket_count
            FROM 
                tickets t
            JOIN 
                companies c ON t.companyid = c.companyid
            GROUP BY 
                c.name;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()