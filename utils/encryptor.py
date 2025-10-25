from cryptography.fernet import Fernet
import unicodedata
import re

def remove_acentos(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

def generate_key():
    return Fernet.generate_key()
def encrypt_data(key, plaintext):
    f = Fernet(key)

    if isinstance(plaintext, memoryview):
        plaintext = bytes(plaintext)

    if isinstance(plaintext, bytes):
        plaintext = plaintext.decode('utf-8', errors='ignore')

    plaintext = remove_acentos(plaintext)
    plaintext_bytes = plaintext.encode('utf-8')

    return f.encrypt(plaintext_bytes)



def decrypt_data(key, ciphertext):
    if isinstance(key, memoryview):
        key = bytes(key)
    if isinstance(ciphertext, memoryview):
        ciphertext = bytes(ciphertext)

    f = Fernet(key)

    try:
        return f.decrypt(ciphertext).decode('utf-8')
    except Exception as e:
        return ciphertext.decode('utf-8', errors='ignore')