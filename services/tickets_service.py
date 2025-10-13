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
    
    def get_tickets_by_status_count(self, start_date: str = None, end_date: str = None):
        """
        Lógica de negócio para obter e formatar a contagem de tickets por status.
        """
        start_date_obj, end_date_obj = self._format_date_range(start_date, end_date)
        results = self.tickets_repository.get_tickets_by_status(start_date_obj, end_date_obj)
        
        tickets_by_status = []
        for row in results:
            status_name, percentage = row
            tickets_by_status.append({
                'status_name': status_name,
                'ticket_count': percentage  # Mantendo como percentage para compatibilidade
            })
        
        return tickets_by_status

    def get_tickets_by_priority(self):
        """
        Lógica de negócio para obter e formatar a contagem de tickets por prioridade.
        """
        results = self.tickets_repository.get_by_priority()
        
        tickets_by_priority = []
        for row in results:
            name, ticket_count = row
            tickets_by_priority.append({
                'name': name,
                'ticket_count': ticket_count
            })
        
        return tickets_by_priority
    
    def get_by_id(self, id: int):
        try:
            return self.tickets_repository.get_by_id(id)
        except Exception as e:
            raise ValueError(str(e))
        
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
        
    def get_tickets_by_department_count(self):
        """Busca e formata a contagem de tickets por departamento."""
        tickets_by_department = self.tickets_repository.get_tickets_by_department()
        return [
            {
                "department_name": department,
                "ticket_count": count
            }
            for department, count in tickets_by_department
        ]
    
    def get_tickets_by_slaplan(self):
        """
        Busca a contagem de tickets por SLAPlan, calcula a porcentagem
        e retorna os resultados formatados.
        """
        result = self.tickets_repository.get_tickets_by_slaplan()
        
        tickets_by_slaplan = []
        for row in result:
            slaplan_name, percentage = row
            tickets_by_slaplan.append({
                'slaplan_name': slaplan_name,
                'percentage': percentage
            })
        
        return result
