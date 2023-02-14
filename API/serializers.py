import pandas as pd
from datetime import datetime


class Serializer:
    serialized_list = []
    d = {
        'day': 'd',
        'week': 'w',
        'month': 'm',
        'hour': 'h',
    }

    def __init__(self, field: str, frequency: str):

        self.serialized_data = {}
        self.__field = field
        self.lower_value, self.upper_value = self.min_max_fields
        self.ts_format = self.get_format(self.d.get(frequency))

    def append_for_period(self, field, data: pd.DataFrame):
        data = data.rename(columns={'ds': 'x', 'yhat': field, 'yhat_lower': self.lower_value,
                                    "yhat_upper": self.upper_value}, inplace=False)

        if 'x' not in self.serialized_data:
            self.serialized_data['x'] = data['x'].apply(datetime.strftime, format=self.ts_format).values.tolist()

        for field in [self.__field, self.lower_value, self.upper_value]:
            self.serialized_data[field] = data[field].apply(round, 1).values.tolist()

    @property
    def min_max_fields(self):
        lower_value, upper_value = f"{self.__field}_lower", f"{self.__field}_upper"
        return lower_value, upper_value

    @staticmethod
    def rename_columns(data: pd.DataFrame):
        return data.rename(columns={'ds': 'x', 'yhat': 'yhat', 'yhat_lower': 'yhat_lower',
                                    "yhat_upper": "yhat_upper"}, inplace=False)

    @staticmethod
    def get_format(frequency: str):
        if frequency in ["d", "w", "M"]:
            return "%Y-%m-%d"
        return "%Y-%m-%d %H:%M:%S"
