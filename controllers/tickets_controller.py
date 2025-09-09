from flask_restx import Namespace, Resource
from services.tickets_service import TicketsService

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
            tickets_service = TicketsService()
            tickets_by_company = tickets_service.get_tickets_by_company_count()
            
            # Retorna a resposta no formato JSON
            return {'data': tickets_by_company}, 200

        except Exception as e:
            return {'error': str(e)}, 500
        
    @tickets_ns.route('/tickets-by-product')
    class TicketsByProduct(Resource):
        def get(self):
            """
            Retorna a quantidade de tickets por produto.
            """
            try:
                tickets_service = TicketsService()
                tickets_by_product = tickets_service.get_tickets_by_product_count()
                return {'data': tickets_by_product}, 200
            except Exception as e:
                return {'error': str(e)}, 500