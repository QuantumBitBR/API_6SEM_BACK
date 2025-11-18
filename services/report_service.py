import json
from services.tickets_service import TicketsService
from utils.report_template import chat_template
from services.gemini_service import GeminiService
from typing import Optional, List, Dict, Any

class ReportService:
    def __init__(self):
        self.tickets_service = TicketsService()
        self.report_template = chat_template
        self.gemini_service = GeminiService()
    
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

    def generate_report(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None):
        
        filter_kwargs = self._get_filter_kwargs(
            company_id, product_id, category_id, priority_id, createdat, end_date
        )
    
        priority_tickets = self.tickets_service.get_tickets_by_priority(**filter_kwargs)
        status_tickets = self.tickets_service.get_tickets_by_status_count(**filter_kwargs)
        company_tickets = self.tickets_service.get_tickets_by_company_count(**filter_kwargs)
        product_tickets = self.tickets_service.get_tickets_by_product_count(**filter_kwargs)
        department_tickets = self.tickets_service.get_tickets_by_department_count(**filter_kwargs)
        category_tickets = self.tickets_service.get_tickets_by_category_count(**filter_kwargs)
        slaplan_tickets = self.tickets_service.get_tickets_by_slaplan(**filter_kwargs)

        payload = {
            "template": self.report_template,
            "dados": {
                "priority_tickets": priority_tickets,
                "status_tickets": status_tickets,
                "company_tickets": company_tickets,
                "product_tickets": product_tickets,
                "department_tickets": department_tickets,
                "category_tickets": category_tickets,
                "slaplan_tickets": slaplan_tickets
            }
        }

        json_payload = json.dumps(payload, ensure_ascii=False, indent=2)

        final_prompt = f'''
        {self.report_template}

        ```json
        {json_payload}
        ```
        '''

        report = self.gemini_service.generate_content(final_prompt)
        return report