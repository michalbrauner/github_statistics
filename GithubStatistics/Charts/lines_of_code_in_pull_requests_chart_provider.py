import pandas as pd
import plotly.graph_objs as go
from GithubStatistics.Charts.chart_provider import ChartProvider


class LinesOfCodeInPullRequestsChartProvider(ChartProvider):
    def get_chart(self, title: str) -> go.Figure:
        pull_requests = self.get_pull_requests_by_datetime_index(self.data, 'merged_at')

        data_rescaled = pull_requests.resample('M')
        additions = data_rescaled['additions'].mean()
        deletions = data_rescaled['deletions'].mean()

        chart_additions = go.Scatter(
            x=additions.index,
            y=additions,
            name='Added',
            mode='lines',
            line={
                'shape': 'spline',
                'color': 'green',
            }
        )

        chart_deletions = go.Scatter(
            x=deletions.index,
            y=deletions,
            name='Deleted',
            mode='lines',
            line={
                'shape': 'spline',
                'color': 'red',
            }
        )

        layout = go.Layout(
            xaxis=dict(
                title='Month',
                tickformat='%B %Y',
                tick0=additions.index[0],
                dtick='M6',
                tickangle=-45
            ),
            yaxis=go.layout.YAxis(
                title='Number of lines'
            ),
            title=title,
        )

        chart_data = [chart_additions, chart_deletions]

        return go.Figure(data=chart_data, layout=layout)

    @staticmethod
    def get_pull_requests_by_datetime_index(data: pd.DataFrame, datetime_column: str):
        pull_requests = data.dropna(subset=[datetime_column], inplace=False, axis='index')

        index = pd.DatetimeIndex(pull_requests[datetime_column])
        pull_requests = pull_requests.set_index(index, drop=True, verify_integrity=False)

        return pull_requests
