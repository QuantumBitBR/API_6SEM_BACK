from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_data(key, plaintext):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    if isinstance(plaintext, memoryview):
        plaintext = bytes(plaintext)
    elif isinstance(plaintext, str):
        # Sempre use UTF-8
        plaintext = plaintext.encode('utf-8')
    return f.encrypt(plaintext)

def decrypt_data(key, ciphertext):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    if isinstance(ciphertext, memoryview):
        ciphertext = bytes(ciphertext)
    return f.decrypt(ciphertext).decode('utf-8')
