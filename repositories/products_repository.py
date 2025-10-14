from config.db_connection import get_cursor
from utils.encryptor import decrypt_data
from datetime import datetime

class ProductsRepository:
    def get_all_products(self):
        """
        Executa a consulta no banco de dados para retornar todos os produtos e seus IDs
        """
        sql_query = """
            SELECT 
                productid, name
            FROM 
                products;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
        
    def get_product_ia(self,):
        sql = """
            SELECT * FROM product_ai
        """

        with get_cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


