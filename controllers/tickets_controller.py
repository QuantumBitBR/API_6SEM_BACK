from flask_restx import Namespace, Resource, fields, reqparse
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

# Definir o parser para os parâmetros de data
date_query_params = reqparse.RequestParser()
date_query_params.add_argument('start_date', 
                              type=str, 
                              required=False, 
                              help='Data inicial no formato YYYY-MM-DD (ex: 2024-01-01)',
                              location='args')
date_query_params.add_argument('end_date', 
                              type=str, 
                              required=False, 
                              help='Data final no formato YYYY-MM-DD (ex: 2024-12-31)',
                              location='args')


filter_parser = reqparse.RequestParser()

filter_parser.add_argument('company_id', type=int, action='split', help='IDs das empresas (separados por vírgula)', required=False)
filter_parser.add_argument('product_id', type=int, action='split', help='IDs dos produtos (separados por vírgula)', required=False)
filter_parser.add_argument('category_id', type=int, action='split', help='IDs das categorias (separados por vírgula)', required=False)
filter_parser.add_argument('priority_id', type=int, action='split', help='IDs das prioridades (separados por vírgula)', required=False)
filter_parser.add_argument('createdat', type=str, help='Data de início do período (YYYY-MM-DD)', required=False)
filter_parser.add_argument('end_date', type=str, help='Data final do período (YYYY-MM-DD)', required=False)


@tickets_ns.route('/tickets-by-company')
class TicketsByCompany(Resource):
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """
        Retorna a quantidade de tickets por empresa, com filtros de ID e período.
        """
        try:
            args = filter_parser.parse_args()
            
            tickets_service = TicketsService()
            
            
            tickets_by_company = tickets_service.get_tickets_by_company_count(
                company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date')
            )
            
            return {'data': tickets_by_company}, 200

        except Exception as e:
            return {'error': str(e)}, 500

        except Exception as e:
            # Lidar com erro
            return {'error': str(e)}, 500
        

@tickets_ns.route('/tickets-by-product')
class TicketsByProduct(Resource):
    @jwt_required
    @cache.cached(timeout=86400)
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
    @jwt_required
    @cache.cached(timeout=86400)
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
    @jwt_required
    @tickets_ns.expect(date_query_params)
    def get(self):
        """
        Retorna a quantidade de tickets por status.
        """
        try:
            args = date_query_params.parse_args()
            start_date = args.get('start_date')
            end_date = args.get('end_date')
            
            tickets_service = TicketsService()
            tickets_by_status = tickets_service.get_tickets_by_status_count(start_date, end_date)
            return {'data': tickets_by_status}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
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
        
@tickets_ns.route('/tickets-by-priority')
class TicketsByStatus(Resource):
    @jwt_required
    @cache.cached(timeout=86400)
    def get(self):
        """
        Retorna a quantidade de tickets por prioridade.
        """
        try:
            tickets_service = TicketsService()
            tickets_by_status = tickets_service.get_tickets_by_priority()
            return {'data': tickets_by_status}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/tickets-by-department')
class TicketsByDepartment(Resource):
    @jwt_required
    @cache.cached(timeout=86400)
    def get(self):
        """Retorna a contagem de tickets por departamento."""
        tickets_service = TicketsService()
        result = tickets_service.get_tickets_by_department_count()
        return {"data": result}
    
@tickets_ns.route('/tickets-by-slaplan')
class TicketsBySLAPlanPercentage(Resource):
    @jwt_required
    @cache.cached(timeout=86400)
    def get(self):
        """Retorna o percentual de tickets por SLAPlan."""
        tickets_service = TicketsService()
        result = tickets_service.get_tickets_by_slaplan()
        return {"data": result}


@tickets_ns.route('/categories')
class TicketCategories(Resource):
    @jwt_required
    @cache.cached(timeout=86400)
    def get(self):
        """Retorna todas as categorias de tickets."""
        tickets_service = TicketsService()
        result = tickets_service.get_all_categories()
        return {"data": result}