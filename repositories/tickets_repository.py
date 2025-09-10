from config.db_connection import get_cursor

class TicketsRepository:
    def get_tickets_by_company(self):
        """
        Executa a consulta no banco de dados para contar os tickets por empresa.
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
    
    ##count tickets by categories and the categories are 1=Sistema, 2=Usuario and 3=Dados

    def get_tickets_by_category(self):
        """
        Executa a consulta no banco de dados para contar os tickets por categoria.
        """
        sql_query = """
            SELECT
                CASE 
                    WHEN categoryid = 1 THEN 'Sistema'
                    WHEN categoryid = 2 THEN 'Usuario'
                    WHEN categoryid = 3 THEN 'Dados'
                    ELSE 'Outros'
                END AS category_name,
                COUNT(ticketid) AS ticket_count
            FROM
                tickets
            GROUP BY
                category_name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()