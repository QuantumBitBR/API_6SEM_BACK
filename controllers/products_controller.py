from flask_restx import Namespace, Resource
from services.products_service import ProductsService

products_ns = Namespace(
    'Products', 
    description='Endpoints relacionados a produtos'
)

@products_ns.route('/all-products')
class AllProducts(Resource):
    def get(self):
        """
        Retorna todos os produtos.
        """
        try:
            products_service = ProductsService()
            data = products_service.get_all_products()
            return {'data': data}, 200

        except Exception as e:
            return {'error': str(e)}, 500
        
@products_ns.route('/all-products-ai')
class AllProducts(Resource):
    def get(self):
        """
        Retorna todos os produtos.
        """
        try:
            products_service = ProductsService()
            data = products_service.get_all_products_ia()
            return {'data': data}, 200

        except Exception as e:
            return {'error': str(e)}, 500