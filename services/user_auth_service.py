from repositories.user_auth_repository import UserAuthRepository
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict, Any
import random, string, re 

import smtplib
from email.message import EmailMessage
from os import environ


sender_email = environ['SENDER_EMAIL']
app_password = environ['APP_PASSWORD']

def send_password_email(receiver_email: str, password: str) -> None:
    """
    Envia a senha temporária para o usuário via Gmail SMTP.
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Sua Senha Temporária de Acesso'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        body = f"""
        Olá,
        
        Seu registro foi concluído com sucesso.
        
        Use a senha temporária abaixo para o seu primeiro login:
        
        Senha Temporária: {password}
        
        Por motivos de segurança, recomendamos que você altere sua senha imediatamente após o login.
        
        Atenciosamente,
        Sua Equipe de Suporte
        """
        msg.set_content(body)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            
        print(f"\n--- SUCESSO: Email enviado para {receiver_email} ---\n")
        
    except Exception as e:
        print(f"\n--- ERRO AO ENVIAR EMAIL ---")
        print(f"Erro: {e}")
        raise RuntimeError(f"Falha ao enviar e-mail: {e}")

def generate_random_password(length=12) -> str:
    """Gera uma senha aleatória com letras, números e símbolos."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def is_valid_email(email: str) -> bool:
    """Valida o formato de um email usando regex simples."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(regex, email)

class UserNotFoundException(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class UserAuthService:
    def __init__(self):
        self.auth_repository = UserAuthRepository()

    def create_new_auth_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Lógica de negócio para criar um novo usuário de autenticação.
        Inclui a CRUCIAL lógica de HASH de senha.
        """
        
        required_fields = ['name', 'email']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"O campo '{field}' é obrigatório.")
            
        email = user_data['email']
        if not is_valid_email(email):
             raise ValueError("O formato do e-mail fornecido é inválido.")
        
        existing_user = self.auth_repository.get_user_by_email(user_data['email'])
        
        if existing_user:
            raise UserAlreadyExistsError("Usuário já existe no sistema.")
                
        user_data['role'] = user_data.get('role', 'user')
        
        temp_password = generate_random_password() 
        hashed_password = generate_password_hash(temp_password)

        user_data['hashed_password'] = hashed_password
        
        new_auth_user_id = self.auth_repository.create_auth_user(user_data)
        
        receiver_email = user_data['email']
        send_password_email(receiver_email, temp_password) 

        return {
            'id': new_auth_user_id, 
            'message': 'Usuário de autenticação criado. Senha temporária enviada por email.'
        }
    
    def delete_auth_user(self, user_id: int) -> None:
        """
        Deleta um usuário de autenticação.
        Levanta UserNotFoundException se o usuário não for encontrado.
        """
        
        rows_affected = self.auth_repository.delete_user_by_id(user_id)
        
        if rows_affected == 0:
            raise UserNotFoundException(f"Usuário com ID {user_id} não foi encontrado.")
            
        return None
    
    def update_auth_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza os dados do usuário, tratando o hash da senha, se necessário.
        """
        
        if 'password' in user_data:
            password = user_data.pop('password')
            user_data['password'] = generate_password_hash(password)
            
        rows_affected = self.auth_repository.update_user(user_id, user_data)
        
        if rows_affected == 0:
            raise UserNotFoundException(f"Usuário com ID {user_id} não foi encontrado.")
            
        return {'id': user_id, 'message': 'Usuário atualizado com sucesso.'}
    
    def get_user_authentication_by_id(self, user_id: int) -> Dict[str, Any]:
        """
        Busca um usuário de autenticação pelo ID.
        Levanta UserNotFoundException se o usuário não for encontrado.
        """
        try:
            user = self.auth_repository.get_user_authentication_by_id(user_id)

            if not user:
                raise UserNotFoundException(f"Usuário com ID {user_id} não foi encontrado.")
            return user, 200
        except UserNotFoundException:
            return {
                "error": "Usuário não encontrado"
            }, 404
        except Exception:
            return {
                "error": "Erro interno do servidor"
            }, 500
        

    def change_user_authentication_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        Altera a senha de um usuário, verificando a senha antiga.
        """
        current_hash = self.auth_repository.get_password_hash_by_id(user_id)

        if not current_hash:
            raise UserNotFoundException(f"Usuário com ID {user_id} não foi encontrado.")

        if not check_password_hash(current_hash, old_password):
            raise InvalidCredentialsException("Senha antiga incorreta.")
            
        hashed_password = generate_password_hash(new_password)
        user_data = {'password': hashed_password} 
        
        rows_affected = self.auth_repository.update_user(user_id, user_data)
        
        if rows_affected == 0:
            raise UserNotFoundException(f"Falha ao atualizar senha. Usuário com ID {user_id} não encontrado.")
            
        return {'id': user_id, 'message': 'Senha alterada com sucesso.'}
            