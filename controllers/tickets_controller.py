from flask_restx import Namespace, Resource, fields, reqparse
from flask import request, make_response
from services.tickets_service import TicketsService
from config.auth import jwt_required
from services.report_service import ReportService
from config.extensions import cache
import time 
import markdown
from flask import make_response
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup

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
filter_parser.add_argument('page', type=int, help='Número da página para paginação', required=False, default=1)

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
    

@tickets_ns.route('/tickets-details')
class AllTickets(Resource):
    @tickets_ns.expect(filter_parser)
    def get(self):
        """
        Retorna todos os tickets com detalhes relacionados, campos descriptografados,
        aplicando filtros e paginação.
        """
        try:
            tickets_service = TicketsService()
            args = filter_parser.parse_args()
            
            all_tickets_data = tickets_service.get_all_tickets_details(
                company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date'),
                page=args.get('page', 1),    
                limit=args.get('limit', 50)   
            )
            return {
                'data': all_tickets_data
            }, 200

        except Exception as e:
            return {'error': str(e)}, 500
    
    
@tickets_ns.route('/report')
class TicketsReport(Resource):
    @tickets_ns.expect(filter_parser) 
    def get(self):
        """Gera um relatório completo de tickets."""
        try:
            report_service = ReportService()
            args = filter_parser.parse_args()
            report = report_service.generate_report(company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date'))
            return {"data": report}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
@tickets_ns.route('/report/pdf')
class TicketsReport(Resource):
    @jwt_required
    @tickets_ns.expect(filter_parser)
    def get(self):
        """Gera relatório completo de tickets em PDF."""
        try:
            report_service = ReportService()
            args = filter_parser.parse_args()

            # 🔥 1. Gera o relatório em Markdown
            markdown_text = report_service.generate_report(
                company_id=args.get('company_id'),
                product_id=args.get('product_id'),
                category_id=args.get('category_id'),
                priority_id=args.get('priority_id'),
                createdat=args.get('createdat'),
                end_date=args.get('end_date')
            )

            # 🔥 2. Converte para HTML
            html_text = markdown.markdown(markdown_text)

            # 🔥 3. Converte HTML → elementos ReportLab
            story = self.convert_html_to_story(html_text)

            # 🔥 4. Gera PDF
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)

            doc.build(story)
            buffer.seek(0)

            # 🔥 5. Retorna o PDF
            response = make_response(buffer.read())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=relatorio_tickets.pdf'
            return response

        except Exception as e:
            return {'error': str(e)}, 500


    # ----------------------------------------------------------------
    # 👇 Função para converter HTML → PDF com títulos, listas e texto
    # ----------------------------------------------------------------
    def convert_html_to_story(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        styles = getSampleStyleSheet()

        story = []

        for elem in soup.children:
            if elem.name in ("h1", "h2", "h3", "h4"):
                style = styles["Heading" + elem.name[1]]  # Heading1, Heading2...
                story.append(Paragraph(elem.text, style))

            elif elem.name == "p":
                story.append(Paragraph(elem.text, styles["Normal"]))

            elif elem.name == "ul":
                items = [
                    ListItem(Paragraph(li.text, styles["Normal"]))
                    for li in elem.find_all("li", recursive=False)
                ]
                story.append(ListFlowable(items, bulletType="bullet"))

            elif elem.name == "ol":
                items = [
                    ListItem(Paragraph(li.text, styles["Normal"]))
                    for li in elem.find_all("li", recursive=False)
                ]
                story.append(ListFlowable(items, bulletType="1"))

            else:
                # fallback: texto direto
                if elem.string and elem.string.strip():
                    story.append(Paragraph(elem.string, styles["Normal"]))

            story.append(Paragraph("<br/>", styles["Normal"]))  # espaçamento

        return story