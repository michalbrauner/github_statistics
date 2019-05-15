import json
import re
import ssl
import sys
import urllib.request
import urllib.response
from http import cookiejar
from http.client import HTTPResponse
from typing import List

class GithubApiClient(object):
    API_URL = 'https://api.github.com'

    def __init__(self, username: str, token: str):
        self._username = username
        self._token = token

    @property
    def username(self):
        return self._username

    @property
    def token(self):
        return self._token

    def get_pull_requests(self):
        data_all = []

        url = '{}/repos/BrandEmbassy/platform-backend/pulls?state=all'.format(self.API_URL)

        current_page = 1

        while True:
            print('Loading page {}'.format(current_page), end='\r')
            sys.stdout.flush()

            response = self.make_request_to_github(url)

            links = self.parse_links(response.headers.get('Link'))
            data_for_this_page = self.append_detailed_data_about_pull_requests(json.loads(response.read()))
            data_all = data_all + data_for_this_page

            if 'next' in links:
                url = links['next']
                current_page = current_page + 1
            else:
                break

        return data_all

    def make_request_to_github(self, url: str) -> HTTPResponse:
        password_manager = urllib.request.HTTPPasswordMgrWithPriorAuth()
        password_manager.add_password(None, url, self.username, self.token, is_authenticated=True)

        request_opener = self.create_request_opener(password_manager)
        request = urllib.request.Request(url=url, method='GET')

        return request_opener.open(request)

    def append_detailed_data_about_pull_requests(self, pull_requests_data: List[dict]) -> List[dict]:
        detailed_pull_requests_data = []

        for pull_request_data in pull_requests_data:
            pull_request_detail = self.get_detail_data_from_pull_request(pull_request_data)

            pull_request_data_final = pull_request_data
            pull_request_data_final['detail_info'] = pull_request_detail

            detailed_pull_requests_data.append(pull_request_data_final)

            break

        return detailed_pull_requests_data

    def get_detail_data_from_pull_request(self, pull_request_data: dict) -> dict:
        response = self.make_request_to_github(pull_request_data['url'])
        pull_request_detail = json.loads(response.read())

        return pull_request_detail

    @staticmethod
    def parse_links(links_from_header: str) -> dict:
        links = {}

        search_data = re.findall(r'<([^>]*)>; rel=\"([\w]+)\"', links_from_header, re.MULTILINE)

        for search_data_item in search_data:
            links[search_data_item[1]] = search_data_item[0]

        return links

    def create_request_opener(self, password_manager: urllib.request.HTTPPasswordMgr):
        ctx = self.get_ssl_default_context()

        opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(debuglevel=0),
            urllib.request.HTTPSHandler(context=ctx, debuglevel=0),
            urllib.request.HTTPCookieProcessor(cookiejar.CookieJar()),
            urllib.request.HTTPBasicAuthHandler(password_manager),
        )

        return opener

    @staticmethod
    def get_ssl_default_context():
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
