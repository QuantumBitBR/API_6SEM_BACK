from flask_restx import Namespace, Resource, fields, marshal_with
from config.opensearch_indexer import OpenSearchIndexer
from flask import request
from services.indexer_service import IndexService

indexes_ns = Namespace(
    'indexes',
    description= "Endpoints responsible for indexer the data in OpenSearch"
)

indexer = OpenSearchIndexer()
indexer_service = IndexService(indexer)

task_model = indexes_ns.model('Task', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String
})

@indexes_ns.route("/search")
class Search(Resource):
    @indexes_ns.marshal_list_with(task_model)
    def get(self):
        q = request.args.get("q", "")
        results = indexer_service.search(q)
        return results

@indexes_ns.route("/reindex")
class Index(Resource):
    def post(self):
        indexer_service.index_tasks()
        return "", 204