from config.db_connection import get_cursor
from typing import Dict, Any, Optional
        
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
        
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca um usuário pelo email. Retorna None se não for encontrado.
        """
        sql_select = "SELECT id, email FROM user_authentication WHERE email = %s;"
        
        with get_cursor() as cur:
            cur.execute(sql_select, (email,))
            result = cur.fetchone()
            
            if result:
                return {'id': result[0], 'email': result[1]} 
            return None
        
    def delete_user_by_id(self, user_id: int) -> int:
        """
        Deleta um usuário da tabela 'user_authentication' pelo ID.
        Retorna o número de linhas afetadas (0 ou 1).
        """
        sql_delete = """
            DELETE FROM user_authentication
            WHERE id = %s;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_delete, (user_id,))
            return cur.rowcount
        
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> int:
        """
        Atualiza dados de um usuário na tabela 'user_authentication' pelo ID.
        Retorna o número de linhas afetadas (0 ou 1).
        """
        set_parts = []
        params = []
        
        updatable_fields = ['name', 'role', 'email', 'password']
        
        for field in updatable_fields:
            if field in user_data:
                set_parts.append(f"{field} = %s")
                params.append(user_data[field])

        if not set_parts:
            return 0 
        
        sql_update = f"""
            UPDATE user_authentication
            SET {', '.join(set_parts)}
            WHERE id = %s;
        """
        
        params.append(user_id)
        
        with get_cursor() as cur:
            cur.execute(sql_update, tuple(params))
            return cur.rowcount


    def get_all_auth_users(self, limit: int = 10, offset: int = 0) -> list:
        """
        Retorna uma lista de todos os usuários na tabela 'user_authentication'.
        """
        sql_select = """SELECT id, name, role, email
        FROM user_authentication
        ORDER BY id DESC
        LIMIT %s OFFSET %s;
        """
        with get_cursor() as cur:
            cur.execute(sql_select, (limit, offset))
            results = cur.fetchall()
            return [{
                'id': row[0],
                'name': row[1],
                'role': row[2],
                'email':row[3],
            } for row in results]
            return users
    
    def count_all_auth_users(self) -> int:
        """
        Retorna o número total de usuários na tabela 'user_authentication'.
        """
        sql_count = "SELECT COUNT(*) FROM user_authentication;"
        
        with get_cursor() as cur:
            cur.execute(sql_count)
            total = cur.fetchone()[0]
            return total
        

        
    def get_user_authentication_by_id(self, userid: int):
        sql_query = """
            SELECT id,name,role,email
            FROM user_authentication where id = %s
        """

        with get_cursor() as cur:
            cur.execute(sql_query, (userid,))
            row = cur.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "email": row[3]
                }             
                    
            return None
        
    def get_password_hash_by_id(self, user_id: int) -> Optional[str]:
        """
        Busca a senha hashada de um usuário pelo ID.
        Retorna a string hashada ou None se o usuário não for encontrado.
        """
        sql_select = "SELECT password FROM user_authentication WHERE id = %s;"
        
        with get_cursor() as cur:
            cur.execute(sql_select, (user_id,))
            result = cur.fetchone()
            
            if result:
                return result[0] 
            return None
        

    # endpoint para enviar email com uma nova senha temporaria para um usuario buscando por id
    def get_user_email_by_id(self, user_id: int) -> Optional[str]:
        """
        Busca o email de um usuário pelo ID.
        Retorna a string do email ou None se o usuário não for encontrado.
        """
        sql_select = "SELECT email FROM user_authentication WHERE id = %s;"
        
        with get_cursor() as cur:
            cur.execute(sql_select, (user_id,))
            result = cur.fetchone()
            
            if result:
                # Retorna apenas o email
                return result[0] 
            return None

