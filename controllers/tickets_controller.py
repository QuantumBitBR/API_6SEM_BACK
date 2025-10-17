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


filter_parser = reqparse.RequestParser()

# Corrigindo os parâmetros para usar type=str e depois converter manualmente
filter_parser.add_argument('company_id', type=str, help='IDs das empresas (separados por vírgula)', required=False)
filter_parser.add_argument('product_id', type=str, help='IDs dos produtos (separados por vírgula)', required=False)
filter_parser.add_argument('category_id', type=str, help='IDs das categorias (separados por vírgula)', required=False)
filter_parser.add_argument('priority_id', type=str, help='IDs das prioridades (separados por vírgula)', required=False)
filter_parser.add_argument('createdat', type=str, help='Data de início do período (YYYY-MM-DD)', required=False)
filter_parser.add_argument('end_date', type=str, help='Data final do período (YYYY-MM-DD)', required=False)


def parse_comma_separated_ids(id_string):
    """Converte string de IDs separados por vírgula em lista de inteiros"""
    if not id_string:
        return None
    try:
        return [int(id.strip()) for id in id_string.split(',') if id.strip().isdigit()]
    except (ValueError, AttributeError):
        return None


@tickets_ns.route('/tickets-by-company')
class TicketsByCompany(Resource):
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """
        Retorna a quantidade de tickets por empresa, com filtros de ID e período.
        """
        try:
            args = filter_parser.parse_args()
            
            # Converter strings para listas de inteiros
            company_ids = parse_comma_separated_ids(args.get('company_id'))
            product_ids = parse_comma_separated_ids(args.get('product_id'))
            category_ids = parse_comma_separated_ids(args.get('category_id'))
            priority_ids = parse_comma_separated_ids(args.get('priority_id'))
            
            tickets_service = TicketsService()
            
            tickets_by_company = tickets_service.get_tickets_by_company_count(
                company_id=company_ids,
                product_id=product_ids,
                category_id=category_ids,
                priority_id=priority_ids,
                createdat=args.get('createdat'),
                end_date=args.get('end_date')
            )
            
            return {'data': tickets_by_company}, 200

        except Exception as e:
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
    
    @tickets_ns.expect(filter_parser)
    def get(self):
        """
        Retorna a quantidade de tickets por status, com filtros de ID e período.
        """
        try:
            args = filter_parser.parse_args()
            
            # Converter strings para listas de inteiros
            company_ids = parse_comma_separated_ids(args.get('company_id'))
            product_ids = parse_comma_separated_ids(args.get('product_id'))
            category_ids = parse_comma_separated_ids(args.get('category_id'))
            priority_ids = parse_comma_separated_ids(args.get('priority_id'))
            
            tickets_service = TicketsService()
            
            tickets_by_status = tickets_service.get_tickets_by_status_count(
                company_id=company_ids,
                product_id=product_ids,
                category_id=category_ids,
                priority_id=priority_ids,
                createdat=args.get('createdat'),
                end_date=args.get('end_date')
            )
            
            return {'data': tickets_by_status}, 200

        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/tickets-by-priority')
class TicketsByPriority(Resource):
    @jwt_required
    @cache.cached(timeout=86400)
    def get(self):
        """
        Retorna a quantidade de tickets por prioridade.
        """
        try:
            tickets_service = TicketsService()
            tickets_by_priority = tickets_service.get_tickets_by_priority()
            return {'data': tickets_by_priority}, 200
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