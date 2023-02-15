import pandas as pd
from matplotlib import pyplot
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

from Prediction.enums import Frequency


class Model:

    def __init__(self, data: pd.DataFrame, period_to_forecast: int, frequency: str):
        """
        The main class for the data processing.
        Here we will process the data and prepare it for the Prophet model which we also create.
        """
        self.data = data
        self.model = Prophet()
        self.period_to_forecast = period_to_forecast
        self.frequency = Frequency.get_frequency(frequency)

    def train(self):
        # fit the model
        self.model.fit(self.data)
        self.model.plot(self.model.predict(self.data))
        print(self.frequency)
        future = self.model.make_future_dataframe(periods=self.period_to_forecast,
                                                  freq=self.frequency)
        """
        Here we are removing setting the floor and the cap to 0 and the max value of the data in order to avoid
        the Prophet model to predict negative values. 
        
        It's very important to set the floor and the cap to the
        real values in order to get the best and the most appropriate results.
        """
        future['floor'] = 0
        forecast = self.model.predict(future)

        return_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']][-self.period_to_forecast:]
        return return_data
