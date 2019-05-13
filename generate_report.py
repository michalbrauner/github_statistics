import argparse
import json

from GithubStatistics.github_statistics import GithubStatisticsProvider
from GithubStatistics.json_to_dataframe_converter import JsonToDataFrameConverter
from ReportGenerator.report_generator import ReportGenerator


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-d', '--data-in-json', type=str, required=True)

    return parser


def main() -> None:
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()

    with open(arguments.data_in_json, 'r') as input_file:
        pull_requests = json.load(input_file)

    pull_requests_as_dataframe = JsonToDataFrameConverter.get_dataframe(pull_requests)
    github_statistics = GithubStatisticsProvider(pull_requests_as_dataframe)

    report_generator = ReportGenerator()
    report_generator.generate(github_statistics, arguments.output)

    print('Report saved.')


if __name__ == "__main__":
    main()

