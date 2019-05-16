import argparse
import json

from GithubApiClient.github_api_client import GithubApiClient


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-r', '--repository', type=str, required=True)
    parser.add_argument('-u', '--github-username', type=str, required=True)
    parser.add_argument('-t', '--github-token', type=str, required=True)
    parser.add_argument('-s', '--page-start', type=int, required=False, default=1)
    parser.add_argument('-e', '--page-end', type=int, required=False, default=99999)

    return parser


def main() -> None:
    argument_parser = get_argument_parser()
    arguments = argument_parser.parse_args()

    client = GithubApiClient(arguments.github_username, arguments.github_token)
    pull_requests = client.get_pull_requests(arguments.page_start, arguments.page_end)

    with open(arguments.output, 'w') as output_file:
        json.dump(pull_requests, output_file)

    print('Data saved in {}'.format(arguments.output))


if __name__ == "__main__":
    main()

