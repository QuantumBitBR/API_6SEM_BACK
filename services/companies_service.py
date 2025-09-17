from repositories.companies_repository import CompaniesRepository

class CompaniesService:
    def __init__(self):
        self.companies_repository = CompaniesRepository()

    def get_companies_with_users_list(self):
        companies_with_users = self.companies_repository.get_companies_with_users()
        
        companies = {}
        for company_name, user_fullname in companies_with_users:

            company_name_str = str(company_name)
            user_fullname_str = str(user_fullname)
            
            if company_name not in companies:
                companies[company_name] = []
            companies[company_name].append(user_fullname)
            
        result = [
            {
                "company_name": company,
                "users": users
            }
            for company, users in companies.items()
        ]
        
        return result