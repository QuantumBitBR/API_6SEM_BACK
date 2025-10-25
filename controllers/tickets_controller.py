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

filter_parser.add_argument('company_id', type=int, action='split', help='IDs das empresas (separados por vírgula)', required=False)
filter_parser.add_argument('product_id', type=int, action='split', help='IDs dos produtos (separados por vírgula)', required=False)
filter_parser.add_argument('category_id', type=int, action='split', help='IDs das categorias (separados por vírgula)', required=False)
filter_parser.add_argument('priority_id', type=int, action='split', help='IDs das prioridades (separados por vírgula)', required=False)
filter_parser.add_argument('createdat', type=str, help='Data de início do período (YYYY-MM-DD)', required=False)
filter_parser.add_argument('end_date', type=str, help='Data final do período (YYYY-MM-DD)', required=False)

def make_cache_key_with_filters():
    return request.url

@tickets_ns.route('/tickets-by-company')
class TicketsByCompany(Resource):
    @jwt_required
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
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """
        Retorna a quantidade de tickets por produto, com filtros.
        """
        try:
            args = filter_parser.parse_args()
            tickets_service = TicketsService()
        
            results = tickets_service.get_tickets_by_product_count(
                company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date')
            )
            
            return {'data': results}, 200

        except Exception as e:
            return {'error': str(e)}, 500


@tickets_ns.route('/tickets-by-category')
class TicketsByCategory(Resource):
    @jwt_required
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """
        Retorna a quantidade de tickets por categoria, com filtros.
        """
        try:
            args = filter_parser.parse_args()
            tickets_service = TicketsService()
            
            # Chama o service, repassando todos os argumentos do parser
            results = tickets_service.get_tickets_by_category_count(
                company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date')
            )
            
            return {'data': results}, 200

        except Exception as e:
            return {'error': str(e)}, 500
        

@tickets_ns.route('/tickets-by-status')
class TicketsByStatus(Resource):
    @jwt_required
    @tickets_ns.expect(filter_parser)
    def get(self):
        """
        Retorna a quantidade de tickets por status.
        """

        args = filter_parser.parse_args()

        try:
            tickets_service = TicketsService()
            tickets_by_status = tickets_service.get_tickets_by_status_count(
                company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date'))
            
            return {'data': tickets_by_status}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/find-tickets-key-word')
class TicketsByKeyWord(Resource):
    @jwt_required
    @tickets_ns.expect(ticket_search_model, validate=True)
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
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """
        Retorna a quantidade de tickets por prioridade.
        """
        try:
            tickets_service = TicketsService()
            args = filter_parser.parse_args()
            tickets_by_status = tickets_service.get_tickets_by_priority(company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date'))
            return {'data': tickets_by_status}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/tickets-by-department')
class TicketsByDepartment(Resource):
    @jwt_required
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """Retorna a contagem de tickets por departamento."""
        try:
            tickets_service = TicketsService()
            args = filter_parser.parse_args()
            result = tickets_service.get_tickets_by_department_count(company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date'))
            return {"data": result}, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
@tickets_ns.route('/tickets-by-slaplan')
class TicketsBySLAPlanPercentage(Resource):
    @jwt_required
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """Retorna o percentual de tickets por SLAPlan."""
        try:

            tickets_service = TicketsService()
            args = filter_parser.parse_args()
            result = tickets_service.get_tickets_by_slaplan(company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date'))
            return {"data": result}
        except Exception as e:
            return {'error': str(e)}, 500


@tickets_ns.route('/categories')
class TicketCategories(Resource):
    @jwt_required
    @tickets_ns.expect(filter_parser)
    def get(self):
        """Retorna todas as categorias de tickets."""
        tickets_service = TicketsService()
        result = tickets_service.get_all_categories()
        return {"data": result}