import datetime
import pandas as pd
import plotly.plotly as py
import plotly.tools

from GithubStatistics.Charts.lines_of_code_in_pull_requests_chart_provider import LinesOfCodeInPullRequestsChartProvider
from GithubStatistics.Charts.open_and_merged_pull_requests_chart_provider import OpenAndMergedPullRequestsChartProvider
from GithubStatistics.github_statistics import GithubStatisticsProvider
from ReportGenerator.github_statistics_to_html_printer import GithubStatisticsToHtmlPrinter

plotly.tools.set_credentials_file(username='michalbrauner', api_key='nueZsBmz2b8joHTjTr9x')


class ReportGenerator(object):
    @staticmethod
    def generate(github_statistics_provider: GithubStatisticsProvider, output_file: str) -> None:
        file_opened = open(output_file, 'w')
        file_opened.write(ReportGenerator.get_html_string(github_statistics_provider))
        file_opened.close()

    @staticmethod
    def get_html_string(github_statistics_provider: GithubStatisticsProvider) -> str:
        generated_at_string = 'Generated at {}'.format(datetime.datetime.now())

        merged_pull_requests_in_time = GithubStatisticsToHtmlPrinter.print_chart(
            ReportGenerator.create_merged_and_created_pull_requests_chart_url(github_statistics_provider.data)
        )

        number_of_lines_in_pull_requests_in_time = GithubStatisticsToHtmlPrinter.print_chart(
            ReportGenerator.create_number_of_lines_in_pull_requests_chart_url(github_statistics_provider.data)
        )

        return '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        ''' + merged_pull_requests_in_time + '''
        ''' + number_of_lines_in_pull_requests_in_time + '''
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
