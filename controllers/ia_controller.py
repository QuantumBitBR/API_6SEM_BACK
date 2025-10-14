from flask_restx import Namespace, Resource, fields
from flask import request
from services.user_service import UserService
from models.user import user_schema
from config.auth import jwt_required
from config.ai_config import ProphetModel

ia_ns = Namespace(
    'Inteligência Artificial',
    description='Endpoints relacionados a inteligência artificial'
)

@ia_ns.route('/tendencia')
class GetTendencia(Resource):
    @ia_ns.doc(params={
        'period': {
            'description': 'Quantidade de previsões futuras',
            'type': 'int',
            'required': False
        },
        'freq': {
            'description': 'Frequência da previsão (YE - year | ME - month | D - day)',
            'type': 'string',
            'required': False
        },
        'start_date': {
            'description': 'A partir de qual data gostaria de ver as previsões com os dados passados',
            'type': 'string',
            'required': False
        },
        'product_id': {
            'description': 'Id do Produto que deve ser filtrado',
            'type': 'int',
            'required': False
        }

    })
    def get(self,):
        try:
            period = request.args.get("period", type=int)
            freq = request.args.get("freq", type=str)
            start_date = request.args.get("start_date", type=str)
            id_model = request.args.get("id_model", type=int)

            model = ProphetModel()
            kwargs = {}

            if period is not None:
                kwargs['period'] = period
            if freq is not None:
                kwargs['freq'] = freq
            if start_date is not None:
                kwargs['start_date'] = start_date
            if id_model is not None:
                kwargs['id_model'] = id_model

            data = model.predict_future(**kwargs)
            data['ds'] = data['ds'].dt.strftime('%Y-%m-%d')
            return {"data": data.to_dict(orient="records")}, 200
        except Exception as error:
            return {"error": str(error)}, 500
