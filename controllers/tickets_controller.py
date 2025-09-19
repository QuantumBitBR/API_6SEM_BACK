from flask_restx import Namespace, Resource
from services.tickets_service import TicketsService
from config.auth import jwt_required

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
            
            return {'data': tickets_by_company}, 200

        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/tickets-by-product')
class TicketsByProduct(Resource):
    @jwt_required
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
        
@tickets_ns.route('/tickets-by-category')
class TicketsByCategory(Resource):
    def get(self):
        """
        Retorna a quantidade de tickets por categoria.
        """
        try:
            tickets_service = TicketsService()
            tickets_by_category = tickets_service.get_tickets_by_category_count()
            return {'data': tickets_by_category}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/tickets-by-status')
class TicketsByStatus(Resource):
    def get(self):
        """
        Retorna a quantidade de tickets por status.
        """
        try:
            tickets_service = TicketsService()
            tickets_by_status = tickets_service.get_tickets_by_status_count()
            return {'data': tickets_by_status}, 200
        except Exception as e:
            return {'error': str(e)}, 500