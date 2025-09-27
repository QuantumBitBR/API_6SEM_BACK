from flask_restx import Namespace, Resource, fields
from flask import request
from services.tickets_service import TicketsService
from config.auth import jwt_required

from config.extensions import cache
import time 
tickets_ns = Namespace(
    'tickets', 
    description='Endpoints relacionados a tickets'
)
ticket_search_model = tickets_ns.model('TicketSearch', {
    'keyword': fields.String(required=True, description='Palavra-chave para buscar nos tickets')
})


@tickets_ns.route('/tickets-by-company')

class TicketsByCompany(Resource):
    @cache.cached(timeout=86400)
    @jwt_required
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
    @cache.cached(timeout=86400)
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
    
    @cache.cached(timeout=86400)
    @jwt_required
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
    @cache.cached(timeout=86400)
    @jwt_required
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
        
@tickets_ns.route('/find-tickets-key-word')
class TicketsByKeyWord(Resource):
    @tickets_ns.expect(ticket_search_model, validate=True)
    @jwt_required
    def post(self):
        try:
            tickets_service = TicketsService()
            request_body = request.get_json()
            key_word = request_body.get('keyword') if request_body else None

            return tickets_service.get_tickets_by_key_word(key_word)
        except Exception as e:
            return {'error': str(e)}, 500