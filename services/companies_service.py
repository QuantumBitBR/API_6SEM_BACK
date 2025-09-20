from repositories.companies_repository import CompaniesRepository
from utils.encryptor import decrypt_data  # função utilitária

class CompaniesService:
    def __init__(self):
        self.companies_repository = CompaniesRepository()

    def get_companies_with_users_data(self):
        """
        Retorna empresas apenas com nome + lista de nomes de funcionários descriptografados.
        """
        results = self.companies_repository.get_companies_with_users_data()
        
        companies = {}
        for row in results:
            (companyid, company_name, userid, fullname_enc, key_encrypt) = row

            try:
                fullname = decrypt_data(key_encrypt, fullname_enc)
            except Exception as e:
                fullname = f"ERRO ao descriptografar ({e})"

            if company_name not in companies:
                companies[company_name] = {
                    "company_name": company_name,
                    "users": []
                }

            companies[company_name]["users"].append(fullname)
        
        return list(companies.values())
