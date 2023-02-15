from dataclasses import Field
from typing import Optional, Tuple, List

import pandas as pd
from pandas import DataFrame


class Data:

    def __init__(self, original_data: pd.DataFrame):
        """
        The main class for the data processing.
        Here we will process the data and prepare it for the Prophet model.
        As it requires the data in a specific format, we need to clean it up and prepare it for the model.

        :param original_data: The original data from the json file.
        """
        self.original_data = original_data
        """
        yhat - The forecasted value of our metric (y) at the date (ds)
        yhat_lower - The lower bound of our forecasts
        yhat_upper - The upper bound of our forecasts

        По факту, мы можем использовать yhat_lower и yhat_upper для того, чтобы понять, насколько точны наши прогнозы.
        Если yhat_lower и yhat_upper находятся в пределах y, то  можем сказать, что прогноз точный.

                    ds       yhat  yhat_lower  yhat_upper
        171 2023-02-06  27.454010   -9.117108   62.349224
        172 2023-02-07  29.463093   -6.959259   64.551996
        173 2023-02-08  31.472177   -3.982182   63.477517
        174 2023-02-09  33.481260   -1.747542   67.575251
        175 2023-02-10  35.490343    0.355324   68.711358
        """

        """
        Here we will create the ds columns which is required by the Prophet model.
        """
        # TODO change to enums

        self.ds = self.create_ds_column()
        self.uniques_with_ds = pd.DataFrame()
        self.visits_with_ds = pd.DataFrame()
        self.sdur_with_ds = pd.DataFrame()
        self.process_data()

    def create_ds_column(self) -> pd.Series:
        return pd.to_datetime(self.original_data['x'])

    def change_uniques_to_y(self) -> None:
        self.uniques_with_ds['ds'] = self.ds
        self.uniques_with_ds['y'] = self.original_data['uniques'].astype(int)

    def change_visits_to_y(self) -> None:
        self.visits_with_ds['ds'] = self.ds
        self.visits_with_ds['y'] = self.original_data["visits"].astype(int)

    def change_sdur_to_y(self) -> None:
        self.sdur_with_ds['ds'] = self.ds
        self.sdur_with_ds['y'] = self.original_data["sdur"].astype(int)

    def process_data(self):
        self.change_visits_to_y()
        self.change_uniques_to_y()
        self.change_sdur_to_y()

    # generate thre dataframes for the model training
    """
    x, uniques_with_ds , x, visits_with_ds, x, sdur_with_ds
    """

    def generate_dataframes(self) -> list[DataFrame]:
        # TODO there is definitely a better way to do this
        return [self.visits_with_ds, self.uniques_with_ds, self.sdur_with_ds]

    def clear_ds(self):
        self.visits_with_ds = self.visits_with_ds.drop(columns=['ds'])
        self.uniques_with_ds = self.uniques_with_ds.drop(columns=['ds'])
        self.sdur_with_ds = self.sdur_with_ds.drop(columns=['ds'])
