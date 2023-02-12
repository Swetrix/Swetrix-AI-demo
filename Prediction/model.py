import pandas as pd
from matplotlib import pyplot
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly


class Model:
    def __init__(self, data: pd.DataFrame, period_to_forecast: int, frequency: str):
        """
        The main class for the data processing.
        Here we will process the data and prepare it for the Prophet model which we also create.
        """
        self.data = data
        self.model = Prophet()
        self.period_to_forecast = period_to_forecast
        self.frequency = frequency

    def train(self):
        # fit the model
        self.model.fit(self.data)
        self.model.plot(self.model.predict(self.data))

        future = self.model.make_future_dataframe(periods=self.period_to_forecast,
                                                  freq=self.frequency)
        forecast = self.model.predict(future)
        # print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        return_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][-self.period_to_forecast:]
        return return_data
