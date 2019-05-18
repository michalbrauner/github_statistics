import datetime

import pandas as pd
import plotly.graph_objs as go
from GithubStatistics.Charts.chart_provider import ChartProvider


class SizeOfPullRequestsByPeopleChartProvider(ChartProvider):
    def get_chart(self, title: str) -> go.Figure:
        pull_requests = self.get_pull_requests_by_datetime_index(self.data, 'merged_at')
        pull_requests['size_of_pull_request'] = pull_requests['additions'] + pull_requests['deletions']

        charts = []
        tick0 = None

        active_after = datetime.datetime.now() - datetime.timedelta(days=240)
        active_after = active_after.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        pull_requests = pull_requests[pull_requests.index >= active_after]

        pull_requests_by_people_grouped = pull_requests.groupby('author_login')
        for author_login, pull_requests_for_user in pull_requests_by_people_grouped:
            data_rescaled = pull_requests_for_user.resample('M')
            size_of_pull_request = data_rescaled['size_of_pull_request'].mean()
            if tick0 is None:
                tick0 = size_of_pull_request.index[0]

            last_activity = size_of_pull_request.index[-1]
            if last_activity < active_after:
                continue

            chart = go.Bar(
                x=size_of_pull_request.index,
                y=size_of_pull_request,
                name=author_login
            )

            charts.append(chart)

        layout = go.Layout(
            xaxis=dict(
                title='Month',
                tickformat='%B %Y',
                tick0=tick0,
                dtick='M1',
                tickangle=-45
            ),
            yaxis=go.layout.YAxis(
                title='Size of lines (added and removed lines)'
            ),
            title=title,
        )

        return go.Figure(data=charts, layout=layout)

    @staticmethod
    def get_pull_requests_by_datetime_index(data: pd.DataFrame, datetime_column: str):
        pull_requests = data.dropna(subset=[datetime_column], inplace=False, axis='index')

        index = pd.DatetimeIndex(pull_requests[datetime_column])
        pull_requests = pull_requests.set_index(index, drop=True, verify_integrity=False)

        return pull_requests
