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
        Retorna todas as empresas junto de seus respectivos usuários.
        """
        try:
            companies_service = CompaniesService()
            data = companies_service.get_companies_with_users_data()
            return {'data': data}, 200

        except Exception as e:
            return {'error': str(e)}, 500

@companies_ns.route('/all-companies')
class AllCompanies(Resource):
    def get(self):
        """
        Retorna todas as empresas.
        """
        try:
            companies_service = CompaniesService()
            data = companies_service.get_all_companies()
            return {'data': data}, 200

        except Exception as e:
            return {'error': str(e)}, 500