from config.opensearch_indexer import OpenSearchIndexer

class IndexService:
    def __init__(self, indexer: OpenSearchIndexer):
        self.indexer = indexer

    def search(self, query: str):
        res = self.indexer.client.search(
            index=self.indexer.index_name,
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
    
    def index_tasks(self):
        self.indexer.index_tasks()