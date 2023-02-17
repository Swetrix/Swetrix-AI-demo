import pandas as pd
from datetime import datetime


class Serializer:
    serialized_list = []

    def __init__(self, field: str, frequency: str):

        self.serialized_data = {}
        self.__field = field
        self.lower_value, self.upper_value = self.min_max_fields
        self.ts_format = self.get_format(frequency)

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

    @staticmethod
    def remove_duplicates(serialized_list):
        seen_keys = set()
        for d in serialized_list:
            for key in list(d.keys()):
                if key in seen_keys:
                    del d[key]
                else:
                    seen_keys.add(key)
        return serialized_list

    @staticmethod
    def swap_visits_and_uniques(processed_data: list[dict]):
        """
        There is the possibility that the Prophet model will predict the uniques to be greater than the visits.
        This function is used to swap the values in case this happens.

        :param processed_data: The list of dictionaries that contains the data for the prediction.
        :return: processed_data
        """

        visits = None
        uniques = None

        for d in processed_data:
            if 'visits' in d:
                visits = d['visits']
            if 'uniques' in d:
                uniques = d['uniques']

        if visits is not None and uniques is not None:
            for i in range(len(visits)):
                if uniques[i] > visits[i]:
                    uniques[i], visits[i] = visits[i], uniques[i]

        for d in processed_data:
            if 'visits' in d:
                d['visits'] = visits
            if 'uniques' in d:
                d['uniques'] = uniques

        return processed_data
