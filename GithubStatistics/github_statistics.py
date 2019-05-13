import pandas as pd
import plotly.graph_objs as go


class GithubStatisticsProvider(object):
    def __init__(self, data: pd.DataFrame):
        self._data = data

    @property
    def data(self):
        return self._data

    def get_merged_pull_requests_in_time_chart(self, title: str) -> go.Figure:
        pull_requests_by_merged_at = self.get_pull_requests_by_merged_at()
        pull_requests_by_created_at = self.get_pull_requests_by_created_at()

        data_by_merged_at_rescaled = pull_requests_by_merged_at.resample('M')
        number_of_pull_requests_by_merged_at = data_by_merged_at_rescaled['number'].count().dropna()

        data_by_created_at_rescaled = pull_requests_by_created_at.resample('M')
        number_of_pull_requests_by_created_at = data_by_created_at_rescaled['number'].count().dropna()

        chart_by_merged_at = go.Scatter(
            x=number_of_pull_requests_by_merged_at.index,
            y=number_of_pull_requests_by_merged_at,
            name='Merged PR',
            mode='lines',
            line={
                'shape': 'spline'
            }
        )

        chart_by_created_at = go.Scatter(
            x=number_of_pull_requests_by_created_at.index,
            y=number_of_pull_requests_by_created_at,
            name='Created PR',
            mode='lines',
            line={
                'shape': 'spline'
            }
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

        chart_data = [chart_by_merged_at, chart_by_created_at]

        return go.Figure(data=chart_data, layout=layout)

    def get_pull_requests_by_merged_at(self):
        pull_requests = self.data.dropna(subset=['merged_at'], inplace=False, axis='index')
        pull_requests = pull_requests.set_index(pd.DatetimeIndex(pull_requests['merged_at']), drop=True,
                                                verify_integrity=False)

        return pull_requests

    def get_pull_requests_by_created_at(self):
        pull_requests = self.data.dropna(subset=['created_at'], inplace=False, axis='index')
        pull_requests = pull_requests.set_index(pd.DatetimeIndex(pull_requests['created_at']), drop=True,
                                                verify_integrity=False)

        return pull_requests
