from opensearchpy import OpenSearch
import os
from config.db_connection import get_cursor
from utils.encryptor import decrypt_data

class OpenSearchIndexer:
    def __init__(self, index_name="tasks", host="localhost", port=9200):
        self.index_name = index_name
        self.client = OpenSearch(
            hosts = [{"host": host, "port": port}],
            http_compress=True,
            http_auth=("admin", "password"),  
            use_ssl=False,                       
            verify_certs=False
        )

    def _ensure_index(self):
        if not self.client.indices.exists(self.index_name):
            self.client.indices.create(
                self.index_name,
                body={
                    "settings": {"number_of_shards": 1},
                    "mappings": {
                        "properties":{
                            "id": {"type": "integer"},
                            "title": {"type": "text"},
                            "description": {"type": "text"}
                        }
                    }
                }
            )

    def index_tasks(self):
        with get_cursor() as cur:
            cur.execute("""SELECT t.ticketid, t.title, t.description, e.keyencrypt 
                        FROM tickets t 
                        INNER JOIN encrypt_ticket e
                        ON e.ticketid = t.ticketid""")
            
            rows = cur.fetchall()

            for task_id, title, description, key in rows:
                doc = {
                        "id": task_id, 
                        "title": decrypt_data(key, title), 
                        "description": decrypt_data(key, description)
                    }
                self.client.index(index=self.index_name, id=task_id, body=doc)

