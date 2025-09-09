from flask_restx import Namespace, Resource
from services.tickets_by_company_service import TicketsByCompanyService

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
            # Chama o serviço para obter os dados formatados
            tickets_service = TicketsByCompanyService()
            tickets_by_company = tickets_service.get_tickets_by_company_count()
            
            # Retorna a resposta no formato JSON
            return {'data': tickets_by_company}, 200

        except Exception as e:
            # Em caso de erro, retorna uma mensagem de erro
            return {'error': str(e)}, 500