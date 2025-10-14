from config.db_connection import get_cursor

class IARepository:
    def __init__(self):
        pass

    def get_product_ia(self,):
        sql = """
            SELECT * FROM product_ai
        """

        with get_cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
        