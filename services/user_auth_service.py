from repositories.user_auth_repository import UserAuthRepository
from werkzeug.security import generate_password_hash
from typing import Dict, Any

import bcrypt

class UserAlreadyExistsError(Exception):
    pass

class UserAuthService:
    def __init__(self):
        self.auth_repository = UserAuthRepository()

    def create_new_auth_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lógica de negócio para criar um novo usuário de autenticação.
        Inclui a CRUCIAL lógica de HASH de senha.
        """
        
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"O campo '{field}' é obrigatório.")
        
        existing_user = self.auth_repository.get_user_by_email(user_data['email'])
        
        if existing_user:
            raise UserAlreadyExistsError("Usuário já existe no sistema.")
                
        user_data['role'] = user_data.get('role', 'user')
        
        password = user_data.pop('password') # Não precisa de .encode('utf-8')
        
        hashed_password = generate_password_hash(password)

        user_data['hashed_password'] = hashed_password
        
        user_data['role'] = user_data.get('role', 'user')
             
        new_auth_user_id = self.auth_repository.create_auth_user(user_data)
        
        return {'id': new_auth_user_id, 'message': 'Usuário de autenticação criado com sucesso.'}