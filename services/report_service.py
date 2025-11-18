import json
from services.tickets_service import TicketsService
from utils.report_template import chat_template
from services.gemini_service import GeminiService

class ReportService:
    def __init__(self):
        self.tickets_service = TicketsService()
        self.report_template = chat_template
        self.gemini_service = GeminiService()

    def generate_report(self):
        priority_tickets = self.tickets_service.get_tickets_by_priority()
        status_tickets = self.tickets_service.get_tickets_by_status_count()
        company_tickets = self.tickets_service.get_tickets_by_company_count()
        product_tickets = self.tickets_service.get_tickets_by_product_count()
        department_tickets = self.tickets_service.get_tickets_by_department_count()
        category_tickets = self.tickets_service.get_tickets_by_category_count()
        slaplan_tickets = self.tickets_service.get_tickets_by_slaplan()

        payload = {
            "prompt": self.report_template,
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