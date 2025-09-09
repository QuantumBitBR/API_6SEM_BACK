from flask_restx import Namespace, Resource
from config.db_connection import get_cursor

# Define um namespace para o endpoint
tickets_ns = Namespace(
    'tickets', 
    description='Endpoints relacionados a tickets'
)

@tickets_ns.route('/tickets-by-company')
class TicketsByCompany(Resource):
    def get(self):
        """
        Retorna a quantidade de tickets por empresa.
        """
        try:
            # SQL para contar os tickets por nome da empresa
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
                results = cur.fetchall()
                
            tickets_by_company = []
            for row in results:
                company_name, ticket_count = row
                tickets_by_company.append({
                    'company_name': company_name,
                    'ticket_count': ticket_count
                })

            return {'data': tickets_by_company}, 200

        except Exception as e:
            # Em caso de erro, retorna uma mensagem de erro
            return {'error': str(e)}, 500
