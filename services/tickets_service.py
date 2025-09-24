from repositories.tickets_repository import TicketsRepository
from services.indexer_service import IndexService
from utils.encryptor import decrypt_data

class TicketsService:
    def __init__(self):
        self.tickets_repository = TicketsRepository()
        self.indexer = IndexService()

    def get_tickets_by_company_count(self):
        """
        Lógica de negócio para obter e formatar a contagem de tickets por empresa.
        """
        results = self.tickets_repository.get_tickets_by_company()
        
        tickets_by_company = []
        for row in results:
            company_name, ticket_count = row
            tickets_by_company.append({
                'company_name': company_name,
                'ticket_count': ticket_count
            })
            
        return tickets_by_company

    def get_tickets_by_product_count(self):
        """
        Lógica de negócio para obter e formatar a contagem de tickets por produto.
        """
        results = self.tickets_repository.get_tickets_by_product()

        tickets_by_product = []
        for row in results:
            product_name, ticket_count = row
            tickets_by_product.append({
                'product_name': product_name,
                'ticket_count': ticket_count
            })
            
        return tickets_by_product
    
    def get_tickets_by_category_count(self):
        """
        Lógica de negócio para obter e formatar a contagem de tickets por categoria.
        """
        results = self.tickets_repository.get_tickets_by_category()

        tickets_by_category = []
        for row in results:
            category_name, ticket_count = row
            tickets_by_category.append({
                'category_name': category_name,
                'ticket_count': ticket_count
            })
            
        return tickets_by_category
    
    def get_tickets_by_status_count(self):
        """
        Lógica de negócio para obter e formatar a contagem de tickets por status.
        """
        results = self.tickets_repository.get_tickets_by_status()
        
        tickets_by_status = []
        for row in results:
            status_name, ticket_count = row
            tickets_by_status.append({
                'status_name': status_name,
                'ticket_count': ticket_count
            })
        
        return tickets_by_status
    
    def get_by_id(self, id: int):
        try:
            return self.tickets_repository.get_by_id(id)
        except Exception as e:
            raise Exception(str(e))
        
    def get_tickets_by_key_word(self, word : str):
        try:
            tickets = self.indexer.search(word)
            tickets_completos = []

            if tickets == []:
                return {
                    "message": "Lista vazia"
                }, 204
            
            for i in tickets:
                tickets_completos.append(self.get_by_id(i['id']))
            
            return {"data": tickets_completos}, 200
        except Exception:
            return {
                'error': 'erro ao tentar buscar os dados'
            }, 500