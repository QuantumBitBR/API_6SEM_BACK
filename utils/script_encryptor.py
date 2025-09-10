from config.db_connection import get_cursor
from utils.encryptor import encrypt_data, generate_key, decrypt_data, remove_acentos

def get_all_users():
    with get_cursor() as cur:
        #cur.execute("SELECT u.email, e.key_encrypt FROM users u inner join encrypt_user e on u.userid = e.id_user")
        cur.execute("SELECT * FROM nova_tabela")
        return cur.fetchall()
    
def update_registers_users(users):
    for i in users:
        key = generate_key()
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE nova_tabela 
                    SET
                    fullname = %s,
                    email = %s,
                    phone = %s,
                    cpf = %s
                    where userid = %s
                """, (
                encrypt_data(key, i[2]),
                encrypt_data(key, i[3]),
                encrypt_data(key, i[4]),
                encrypt_data(key, i[5]),
                i[0]
            ))

            cur.execute(
                """
                INSERT INTO encrypt_user (id_user, key_encrypt) 
                VALUES (%s, %s)
                """,
                (i[0], key),
            )

def descriptografando(users):
    for encrypted_fullname, key in users:
        try:
            print(decrypt_data(key, encrypted_fullname))
        except Exception:
            print("Dado não criptografado ou inválido:", encrypted_fullname)
