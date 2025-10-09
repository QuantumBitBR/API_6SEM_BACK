import pickle
import pandas as pd

class ProphetModel:
    def __init__(self):
        with open('../model_AI/prophet_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
    
    def predict_future(self, months: int = 3, freq: str = 'ME', start_date: str = None) -> pd.DataFrame:
        valid_freqs = ['ME', 'D', 'Y']
        if freq not in valid_freqs:
            freq = 'ME'

        future = self.model.make_future_dataframe(periods=months, freq=freq)
        forecast = self.model.predict(future)
        last_date = self.model.history['ds'].max()

        forecast['is_future'] = forecast['ds'] > last_date
        forecast['year'] = forecast['ds'].dt.year

        if start_date:
            start_date = pd.to_datetime(start_date)
            forecast = forecast[forecast['ds'] >= start_date]

        return forecast[['ds', 'year', 'yhat','is_future']]


pm = ProphetModel()

forecast = pm.predict_future(months=5, freq='Y', start_date='2018-12-01')
print(forecast)
