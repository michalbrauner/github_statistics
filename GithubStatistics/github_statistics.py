import pandas as pd
import plotly.graph_objs as go


class GithubStatisticsProvider(object):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    @property
    def data(self):
        return self._data

    def get_merged_pull_requests_in_time_chart(self, title: str) -> go.Figure:
        data = self.data.dropna(subset=['merged_at'], inplace=False, axis='index')
        data = data.set_index(['merged_at'], drop=True, verify_integrity=True)

        balances_chart = go.Scatter(
            x=data.index,
            y=data,
            name='Date',
            mode='lines'
        )

        layout = go.Layout(
            xaxis=dict(
                title='Date'
            ),
            yaxis=go.layout.YAxis(
                title='Number of pull requests'
            ),
            title=title,
        )

        chart_data = [balances_chart]

        return go.Figure(data=chart_data, layout=layout)
