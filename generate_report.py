import argparse

from GithubApiClient.github_api_client import GithubApiClient
from GithubStatistics.github_statistics import GithubStatisticsProvider
from GithubStatistics.json_to_dataframe_converter import JsonToDataFrameConverter
from ReportGenerator.report_generator import ReportGenerator


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-directory', type=str, required=True)
    parser.add_argument('-r', '--repository', type=str, required=True)
    parser.add_argument('-u', '--github-username', type=str, required=True)
    parser.add_argument('-t', '--github-token', type=str, required=True)

    return parser


def main() -> None:
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()

    client = GithubApiClient(arguments.github_username, arguments.github_token)
    pull_requests = client.get_pull_requests()
    pull_requests_as_dataframe = JsonToDataFrameConverter.get_dataframe(pull_requests)
    github_statistics = GithubStatisticsProvider(pull_requests_as_dataframe)

    report_generator = ReportGenerator()
    report_generator.generate(github_statistics, 'G:\\data_science', 'report.html')


if __name__ == "__main__":
    main()

