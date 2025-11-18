from repositories.tickets_repository import TicketsRepository
from services.indexer_service import IndexService
from utils.encryptor import decrypt_data
from typing import Optional, List, Dict, Any, Union

class TicketsService:
    def __init__(self):
        self.tickets_repository = TicketsRepository()
        self.indexer = IndexService()

    def _get_filter_kwargs(
        self,
        company_id: Optional[List[int]] = None, 
        product_id: Optional[List[int]] = None, 
        category_id: Optional[List[int]] = None, 
        priority_id: Optional[List[int]] = None, 
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Agrupa os parâmetros de filtro em um dicionário para fácil repasse."""
        return {
            'company_id': company_id,
            'product_id': product_id,
            'category_id': category_id,
            'priority_id': priority_id,
            'createdat': createdat,
            'end_date': end_date
        }


    def get_tickets_by_company_count(
        self,
        company_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )

        results = self.tickets_repository.get_tickets_by_company(**filter_kwargs)
        
        tickets_by_company = []
        for row in results:
            company_name, ticket_count = row
            tickets_by_company.append({
                'company_name': company_name,
                'ticket_count': ticket_count
            })
            
        return tickets_by_company

    def get_tickets_by_product_count(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lógica de negócio para obter e formatar a contagem de tickets por produto,
        aplicando filtros.
        """
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )

        results = self.tickets_repository.get_tickets_by_product(**filter_kwargs)
        
        tickets_by_product = []
        for row in results:
            product_name, ticket_count = row
            tickets_by_product.append({
                'product_name': product_name,
                'ticket_count': ticket_count
            })
            
        return tickets_by_product
    
    def get_tickets_by_category_count(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lógica de negócio para obter e formatar a contagem de tickets por categoria,
        aplicando filtros.
        """
        
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )

        results = self.tickets_repository.get_tickets_by_category(**filter_kwargs)
        
        tickets_by_category = []
        for row in results:
            category_name, ticket_count = row
            tickets_by_category.append({
                'category_name': category_name,
                'ticket_count': ticket_count
            })
            
        return tickets_by_category
    
    def get_tickets_by_status_count(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
        ) -> List[Dict[str, Any]]:
        """
        Lógica de negócio para obter e formatar a contagem de tickets por status,
        aplicando filtros.
        """
        
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )

        results = self.tickets_repository.get_tickets_by_status(**filter_kwargs)
        
        tickets_by_status = []
        for row in results:

            status_name, percentage = row 

            tickets_by_status.append({
                'status_name': status_name,
                'percentage': round(percentage, 2) 
            })
            
        return tickets_by_status

    def get_tickets_by_priority(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
        ) -> List[Dict[str, Any]]:
        """
        Lógica de negócio para obter e formatar a contagem de tickets por prioridade.
        """
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )
        results = self.tickets_repository.get_by_priority(**filter_kwargs)
        
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
                ticket_encontrado = self.get_by_id(i['id'])
                if ticket_encontrado != False:
                    tickets_completos.append(ticket_encontrado)
            
            return {"data": tickets_completos}, 200
        except Exception:
            return {
                'error': 'erro ao tentar buscar os dados'
            }, 500
        
    def get_tickets_by_department_count(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
        ) -> List[Dict[str, Any]]:
        """Busca e formata a contagem de tickets por departamento."""
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )
        tickets_by_department = self.tickets_repository.get_tickets_by_department(**filter_kwargs)
        return [
            {
                "department_name": department,
                "ticket_count": count
            }
            for department, count in tickets_by_department
        ]
    
    def get_tickets_by_slaplan(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
        ) -> List[Dict[str, Any]]:
        """
        Busca a contagem de tickets por SLAPlan, calcula a porcentagem
        e retorna os resultados formatados.
        """
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )
        result = self.tickets_repository.get_tickets_by_slaplan(**filter_kwargs)
        
        tickets_by_slaplan = []
        for row in result:
            slaplan_name, percentage = row
            tickets_by_slaplan.append({
                'slaplan_name': slaplan_name,
                'percentage': percentage
            })
        
        return result

    def get_all_tickets_details(
        self,
        company_id: Optional[List[int]] = None, 
        product_id: Optional[List[int]] = None, 
        category_id: Optional[List[int]] = None, 
        priority_id: Optional[List[int]] = None, 
        createdat: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,  
        limit: int = 50  
    ) -> Dict[str, Any]:
        """
        Chama o repositório para buscar tickets paginados, filtrados e com os dados 
        relacionados (nomes) e descriptografados, retornando o formato JSON desejado.
        
        Retorna um dicionário com os dados da página e a lista de tickets.
        """
        
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )
        
        filter_kwargs['page'] = page
        filter_kwargs['limit'] = limit

        return self.tickets_repository.get_all_tickets_details(**filter_kwargs)
    
    def get_all_categories(self):
        """Busca todas as categorias de tickets."""
        categories = self.tickets_repository.get_all_categories()
        return [{"category_id": cat_id, "category_name": cat_name} for cat_id, cat_name in categories]
    
