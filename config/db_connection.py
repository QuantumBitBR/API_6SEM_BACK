import psycopg2
from os import environ
from contextlib import contextmanager

@contextmanager
def get_cursor():
    """
    Context manager que cria a conexão e o cursor do banco de dados.
    Fecha cursor e conexão automaticamente ao final do bloco.
    """
    conn = psycopg2.connect(
        host=environ['DB_URL'],
        database="helpai",
        user=environ['DB_USERNAME'],
        password=environ['DB_PASSWORD']
    )
    try:
        with conn.cursor() as cur:
            yield cur  
        conn.commit()
    finally:
        conn.close()


@contextmanager
def get_cursor_db_keys():
    """
    Context manager que cria a conexão e o cursor do banco de dados das chaves de criptografia.
    Fecha cursor e conexão automaticamente ao final do bloco.
    """
    conn = psycopg2.connect(
        host=environ['DB_URL'],
        database="helpaikeys",
        user=environ['DB_USERNAME'],
        password=environ['DB_PASSWORD']
    )
    try:
        with conn.cursor() as cur:
            yield cur  
        conn.commit()
    except Exception as e:
        print("Erro ao conectar ao banco de chaves:", e)
        raise e
    finally:
        conn.close()