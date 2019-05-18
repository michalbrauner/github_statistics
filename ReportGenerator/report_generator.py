import datetime
import pandas as pd
import plotly.plotly as py
import plotly.tools

from GithubStatistics.Charts.lines_of_code_in_pull_requests_chart_provider import LinesOfCodeInPullRequestsChartProvider
from GithubStatistics.Charts.open_and_merged_pull_requests_chart_provider import OpenAndMergedPullRequestsChartProvider
from GithubStatistics.Charts.size_of_pull_requests_by_people_chart_provider import \
    SizeOfPullRequestsByPeopleChartProvider
from GithubStatistics.github_statistics import GithubStatisticsProvider
from ReportGenerator.github_statistics_to_html_printer import GithubStatisticsToHtmlPrinter


class ReportGenerator(object):
    def __init__(self, plotly_username: str, plotly_api_key: str):
        self._plotly_username = plotly_username
        self._plotly_api_key = plotly_api_key

    @property
    def plotly_username(self) -> str:
        return self._plotly_username

    @property
    def plotly_api_key(self) -> str:
        return self._plotly_api_key

    def generate(self, github_statistics_provider: GithubStatisticsProvider, output_file: str, repository: str) -> None:
        plotly.tools.set_credentials_file(username=self.plotly_username, api_key=self.plotly_api_key)

        file_opened = open(output_file, 'w')
        file_opened.write(self.get_html_string(github_statistics_provider, repository))
        file_opened.close()

    def get_html_string(self, github_statistics_provider: GithubStatisticsProvider, repository: str) -> str:
        generated_at_string = 'Generated at {}'.format(datetime.datetime.now())

        merged_pull_requests_in_time = GithubStatisticsToHtmlPrinter.print_chart(
            ReportGenerator.create_merged_and_created_pull_requests_chart_url(github_statistics_provider.data)
        )

        number_of_lines_in_pull_requests_in_time = GithubStatisticsToHtmlPrinter.print_chart(
            ReportGenerator.create_number_of_lines_in_pull_requests_chart_url(github_statistics_provider.data)
        )

        size_of_pull_requests_by_people_in_time = GithubStatisticsToHtmlPrinter.print_chart(
            ReportGenerator.create_size_of_pull_requests_by_people_chart_url(github_statistics_provider.data)
        )

        return '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Statistics from Github</h1>
        <h3>Repository: ''' + repository + '''</h3>
        ''' + merged_pull_requests_in_time + '''
        ''' + number_of_lines_in_pull_requests_in_time + '''
        ''' + size_of_pull_requests_by_people_in_time + '''
        <hr />
        <div class="row"><div class="col-xs-12 col-sm-12"><em>''' + generated_at_string + '''</em></div></div>
        <br /><br />
    </body>
</html>
        '''

    @staticmethod
    def create_merged_and_created_pull_requests_chart_url(data: pd.DataFrame):
        chart_provider = OpenAndMergedPullRequestsChartProvider(data)
        chart = chart_provider.get_chart('Created and merged pull requests')

        return py.plot(chart, filename='merged_pull_requests_in_time_chart', auto_open=False)

    @staticmethod
    def create_number_of_lines_in_pull_requests_chart_url(data: pd.DataFrame):
        chart_provider = LinesOfCodeInPullRequestsChartProvider(data)
        chart = chart_provider.get_chart('Average number of lines in pull requests / month')

        return py.plot(chart, filename='average_number_of_lines_in_pull_requests_in_time_chart', auto_open=False)

    @staticmethod
    def create_size_of_pull_requests_by_people_chart_url(data: pd.DataFrame):
        chart_provider = SizeOfPullRequestsByPeopleChartProvider(data)
        chart = chart_provider.get_chart(
            'Average size of pull requests / month (last 240 days)')

        return py.plot(chart, filename='average_size_of_pull_requests_by_people_time_chart', auto_open=False)
