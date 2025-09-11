from config.db_connection import get_cursor
from utils.encryptor import encrypt_data, generate_key, decrypt_data, remove_acentos
import csv
def get_all_users():
    with get_cursor() as cur:
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
    
def update_registers_users(users):
    for i in users:
        key = generate_key()
        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE users 
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

def get_tickets():
    with get_cursor() as cur:
        cur.execute("SELECT t.ticketid, t.title, t.description FROM tickets t where ticketid >= 40001 and ticketid <= 45000")
        return cur.fetchall()

def update_registers_tickets(tickets):
    for i in tickets:
        key = generate_key()

        with get_cursor() as cur:
            cur.execute(
                """
                UPDATE tickets
                SET 
                titleencrypt = %s,
                descriptionencrypt = %s
                where ticketid = %s

                """, 
                (encrypt_data(key,i[1]), 
                encrypt_data(key, i[2]), 
                i[0])
            )

            cur.execute("""
                INSERT INTO encrypt_ticket (ticketid, keyencrypt)
                        VALUES (%s, %s)
                """, (i[0], key))
            
def get_tickets_descr():
    with get_cursor() as cur:
        cur.execute("SELECT t.titleencrypt, e.keyencrypt FROM tickets t inner join encrypt_ticket e on e.ticketid = t.ticketid where t.ticketid < 50")
        return cur.fetchall()
    
def descriptografando(users):
    for encrypted_fullname, key in users:
        try:
            print(decrypt_data(key, encrypted_fullname))
        except Exception:
            print("Dado não criptografado ou inválido:", encrypted_fullname)
# descriptografando(get_tickets_descr()) 
update_registers_tickets(get_tickets())