class Frequency:
    values = {
        'day': 'd',
        'week': 'w',
        'month': 'm',
        'hour': 'h',
    }

    @staticmethod
    def get_frequency(frequency: str):
        try:
            return Frequency.values.get(frequency)
        except KeyError:
            return None
