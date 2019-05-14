import pandas as pd
import plotly.graph_objs as go
from abc import ABC, abstractmethod


class ChartProvider(ABC):
    def __init__(self, data: pd.DataFrame):
        self._data = data
        super().__init__()

    @property
    def data(self):
        return self._data

    @abstractmethod
    def get_chart(self, title: str) -> go.Figure:
        pass
