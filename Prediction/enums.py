class Frequency:
    values = {
        'day': 'd',
        'week': 'w',
        'month': 'M',
        'hour': 'h',
    }

    @staticmethod
    def get_frequency(frequency: str):
        try:
            return Frequency.values.get(frequency)
        except KeyError:
            return None
