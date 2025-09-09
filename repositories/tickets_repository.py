from config.db_connection import get_cursor

class TicketsRepository:
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
        
    def get_tickets_by_product(self):
        """
        Executa a consulta no banco de dados para contar os tickets por produto.
        Retorna uma lista de tuplas.
        """
        sql_query = """
            SELECT
                p.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                products p ON t.productid = p.productid
            GROUP BY
                p.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()