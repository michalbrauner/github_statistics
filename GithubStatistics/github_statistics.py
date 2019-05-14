import pandas as pd


class GithubStatisticsProvider(object):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    @property
    def data(self):
        return self._data
