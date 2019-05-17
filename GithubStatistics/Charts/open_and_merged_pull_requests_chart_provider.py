import pandas as pd
import plotly.graph_objs as go
from GithubStatistics.Charts.chart_provider import ChartProvider


class OpenAndMergedPullRequestsChartProvider(ChartProvider):
    def get_chart(self, title: str) -> go.Figure:
        pull_requests_by_merged_at = self.get_pull_requests_by_datetime_index(self.data, 'merged_at')
        pull_requests_by_created_at = self.get_pull_requests_by_datetime_index(self.data, 'created_at')

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
                title='Month',
                tickformat='%B %Y',
                tick0=number_of_pull_requests_by_merged_at.index[0],
                dtick='M6',
                tickangle=-45
            ),
            yaxis=go.layout.YAxis(
                title='Number of pull requests'
            ),
            title=title,
        )

        chart_data = [chart_by_merged_at, chart_by_created_at]

        return go.Figure(data=chart_data, layout=layout)

    @staticmethod
    def get_pull_requests_by_datetime_index(data: pd.DataFrame, datetime_column: str):
        pull_requests = data.dropna(subset=[datetime_column], inplace=False, axis='index')

        index = pd.DatetimeIndex(pull_requests[datetime_column])
        pull_requests = pull_requests.set_index(index, drop=True, verify_integrity=False)

        return pull_requests
