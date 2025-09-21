from cryptography.fernet import Fernet
# Gerar chave (apenas uma vez, salve com segurança)
def generate_key():
    return Fernet.generate_key()

# Criptografar dados
def encrypt_data(key, plaintext):
    f = Fernet(key)
    return f.encrypt(plaintext.encode())

# Descriptografar dados
def decrypt_data(key, ciphertext):
    if isinstance(key, str):
        key = key.encode()
    if isinstance(ciphertext, memoryview):
        ciphertext = ciphertext.tobytes()
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()

key = generate_key()
texto_cript = encrypt_data(key, "texto")
texto_desc = decrypt_data(key, texto_cript)
