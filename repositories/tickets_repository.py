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

    def get_tickets_by_category(self):
        """
        Executa a consulta no banco de dados para contar os tickets por categoria.
        """
        sql_query = """
            SELECT
                ca.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                categories ca ON t.categoryid = ca.categoryid
            GROUP BY
                ca.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()

    def get_tickets_by_status(self):
        """
        Executa a consulta no banco de dados para contar os tickets por status.
        """
        sql_query = """
            SELECT
                s.name,
                COUNT(s.name) AS ticket_count
            FROM
                ticketstatushistory tsh
            JOIN
                statuses s ON tsh.tostatusid = s.statusid
            WHERE
                tsh.historyid IN (
                    SELECT MAX(historyid)
                    FROM ticketstatushistory
                    GROUP BY ticketid
                )
            GROUP BY
                s.name;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()