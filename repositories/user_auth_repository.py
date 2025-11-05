from config.db_connection import get_cursor
from typing import Dict, Any
        
class UserAuthRepository:
    def __init__(self):
        pass

    def create_auth_user(self, user_data: Dict[str, Any]) -> int:
        """
        Executa a inserção de um novo usuário na tabela 'user_authentication'.
        Retorna o 'id' do usuário criado.
        """
        
        sql_insert = """
            INSERT INTO user_authentication (
                name, role, email, password
            ) VALUES (
                %s, %s, %s, %s
            ) RETURNING id;
        """
        
        params = (
            user_data['name'],
            user_data['role'],
            user_data['email'],
            user_data['hashed_password']
        )
        
        with get_cursor() as cur:
            cur.execute(sql_insert, params)
            new_user_id = cur.fetchone()[0]
            return new_user_id