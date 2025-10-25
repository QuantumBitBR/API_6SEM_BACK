from repositories.products_repository import ProductsRepository
from utils.encryptor import decrypt_data

class ProductsService:
    def __init__(self):
        self.products_repository = ProductsRepository()
    
    def get_all_products(self):
        """
        Retorna todos os produtos.
        """
        results = self.products_repository.get_all_products()
        products = []
        for row in results:
            product = {
                "ProductID": row[0],
                "ProductName": row[1]
            }
            products.append(product)
        return products


    def get_all_products_ia(self):
        """
        Retorna todos os produtos.
        """
        results = self.products_repository.get_product_ia()
        products = []
        for row in results:
            product = {
                "ProductID": row[0],
                "ProductName": row[1]
            }
            products.append(product)
        return products