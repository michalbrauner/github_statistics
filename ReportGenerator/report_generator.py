import datetime
import os
import plotly.plotly as py
import plotly.tools
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

        merged_pull_requests_in_time_chart = github_statistics_provider.get_merged_pull_requests_in_time_chart(
            'Merged pull requests')

        merged_pull_requests_in_time_url = py.plot(merged_pull_requests_in_time_chart,
                                                   filename='merged_pull_requests_in_time_chart',
                                                   auto_open=False)

        merged_pull_requests_in_time = GithubStatisticsToHtmlPrinter.print_chart(merged_pull_requests_in_time_url)

        return '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Pull requests statistics</h1>     
        ''' + merged_pull_requests_in_time + '''
        <hr />
        <div class="row"><div class="col-xs-12 col-sm-12"><em>''' + generated_at_string + '''</em></div></div>
        <br /><br />
    </body>
</html>
        '''
