from opensearchpy import OpenSearch, helpers
import os
import re
import logging
from urllib.parse import urlparse
from config.db_connection import get_cursor
from utils.encryptor import decrypt_data
from os import environ

from opensearchpy import helpers
from tqdm import tqdm
logging.basicConfig(level=logging.INFO)

class OpenSearchIndexer:
    def __init__(self, index_name="tickets"):
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
                            "description": {"type": "text"},
                            "company": {"type": "text"},
                            "product": {"type": "text"},
                            "status": {"type": "text"},
                            "category": {"type": "text"},
                            "subcategory": {"type": "text"},
                            "chanel": {"type": "text"},
                            "device": {"type": "text"},
                            "priority": {"type": "text"}

                        }
                    }
                }
            )



    def index_tickets(self, ):
        with get_cursor() as cur:
            cur.execute("""
                SELECT t.ticketid, t.title, t.description, e.keyencrypt, c.name,  
                    p.name, s.name, cat.name, sub.name, t.channel, t.device, prio.name
                FROM tickets t 
                INNER JOIN encrypt_ticket e ON e.ticketid = t.ticketid 
                INNER JOIN companies c ON t.companyid = c.companyid
                INNER JOIN products p ON p.productid = t.productid
                INNER JOIN statuses s ON s.statusid = t.currentstatusid
                INNER JOIN categories cat ON cat.categoryid = t.categoryid
                INNER JOIN subcategories sub ON sub.subcategoryid = t.subcategoryid
                INNER JOIN priorities prio ON prio.priorityid = t.priorityid
                ORDER BY t.ticketid
            """)
            rows = cur.fetchall()

            total = len(rows)
            batch_size = 1000
            actions = []

            print(f"\nTotal de tickets encontrados: {total}\n")

            print(f"Iniciando indexação no índice '{self.index_name}'...\n")

            for i, (task_id, title, description, key, company, product, status, categoria, subcategoria, channel, device, priority) in enumerate(
                tqdm(rows, desc="Indexando tickets", unit="doc"), start=1
            ):
                doc = {
                    "_index": self.index_name,
                    "_id": task_id,
                    "_source": {
                        "id": task_id,
                        "title": decrypt_data(key, title),
                        "description": decrypt_data(key, description),
                        "company": company,
                        "product": product,
                        "status": status,
                        "category": categoria,
                        "subcategory": subcategoria,
                        "channel": channel,
                        "device": device,
                        "priority": priority
                    }
                }
                actions.append(doc)

                if i % batch_size == 0:
                    helpers.bulk(self.client, actions)
                    tqdm.write(f"Lote {i // batch_size} enviado ({i} documentos no total).")
                    actions = []
                    
            if actions:
                helpers.bulk(self.client, actions)
                tqdm.write(f"Último lote enviado ({len(actions)} registros restantes).")

            print("\nIndexação concluída com sucesso!")


    def delete_data(self):
        self.client.delete_by_query(
            index=self.index_name,
            body={"query": {"match_all": {}}}
        )

