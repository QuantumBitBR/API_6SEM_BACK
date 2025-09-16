from opensearchpy import OpenSearch
import os
import re
import logging
from urllib.parse import urlparse
from config.db_connection import get_cursor
from utils.encryptor import decrypt_data
from os import environ

# Configurar logging
logging.basicConfig(level=logging.INFO)

class OpenSearchIndexer:
    def __init__(self, index_name="tasks"):
        self.index_name = index_name

        bonsai = environ['BONSAI_URL']
        auth = re.search(r'https://(.*)@', bonsai).group(1).split(':')
        host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

        match = re.search(r'(:\d+)', host)
        if match:
            p = match.group(0)
            host = host.replace(p, '')
            port = int(p.split(':')[1])
        else:
            port = 443

        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=(auth[0], auth[1]),
            use_ssl=True,
            verify_certs=True,
            ssl_show_warn=True
        )

    def _ensure_index(self):
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(
                index=self.index_name,
                body={
                    "settings": {"number_of_shards": 1},
                    "mappings": {
                        "properties": {
                            "id": {"type": "integer"},
                            "title": {"type": "text"},
                            "description": {"type": "text"}
                        }
                    }
                }
            )

    def index_tasks(self):
        with get_cursor() as cur:
            cur.execute("""
                SELECT t.ticketid, t.title, t.description, e.keyencrypt 
                FROM tickets t 
                INNER JOIN encrypt_ticket e ON e.ticketid = t.ticketid where t.ticketid >=151 and t.ticketid <=1000
            """)
            rows = cur.fetchall()

            for task_id, title, description, key in rows:
                doc = {
                    "id": task_id,
                    "title": decrypt_data(key, title),
                    "description": decrypt_data(key, description)
                }
                self.client.index(index=self.index_name, id=task_id, body=doc)
                print(task_id)

    def search(self, query: str):
        res = self.client.search(
            index=self.index_name,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "description"]
                    }
                }
            }
        )
        return [hit["_source"] for hit in res["hits"]["hits"]]
    
def main():
    indexer = OpenSearchIndexer(index_name="tasks")
    
    if indexer.client.ping():
        print("Conexão com Bonsai Search estabelecida com sucesso!")
        #indexer.index_tasks()
    else:
        print("Falha na conexão com Bonsai Search")
        
if __name__ == "__main__":
    main()