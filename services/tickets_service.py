from repositories.tickets_repository import TicketsByCompanyRepository

class TicketsByCompanyService:
    def __init__(self):
        self.tickets_repository = TicketsByCompanyRepository()

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