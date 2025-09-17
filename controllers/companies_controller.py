from flask_restx import Namespace, Resource
from services.companies_service import CompaniesService


companies_ns = Namespace(
    'companies',
    description='Endpoints relacionados a empresas'
)

@companies_ns.route('/companies-with-users')
class CompaniesWithUsers(Resource):
    def get(self):
        """
        Retorna a lista de empresas com seus respectivos usuários.
        """
        companies_service = CompaniesService()
        result = companies_service.get_companies_with_users_list()
        return {"data": result}