import pickle
import pandas as pd
import os

class ProphetModel:
    def __init__(self, id_model: int = 0):
        if(id_model == 0 or id_model > 18):
            model_path = os.path.join(os.path.dirname(__file__), '../model_AI/prophet_model.pkl')
        else:
            model_path = os.path.join(os.path.dirname(__file__), f'../model_AI/{id_model}_model.pkl')

        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
    
    def predict_future(self, period: int = 10, freq: str = 'D', start_date: str = '2018-01-01') -> pd.DataFrame:
        valid_freqs = ['ME', 'D', 'YE']
        if freq not in valid_freqs:
            freq = 'D'

        future = self.model.make_future_dataframe(periods=period, freq=freq)
        forecast = self.model.predict(future)
        last_date = self.model.history['ds'].max()

        forecast['is_future'] = forecast['ds'] > last_date
        forecast['year'] = forecast['ds'].dt.year

        if start_date:
            start_date = pd.to_datetime(start_date)
            forecast = forecast[forecast['ds'] >= start_date]

        return forecast[['ds', 'year', 'yhat','is_future']]

