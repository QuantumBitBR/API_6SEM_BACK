from config.db_connection import get_cursor

def listar_usuarios():
    with get_cursor() as cur:
        cur.execute("SELECT * FROM agents")
        return cur.fetchall()