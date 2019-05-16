import asyncio
import json
import queue
import re
import ssl
import sys
import urllib.request
import urllib.response
from concurrent.futures import ThreadPoolExecutor
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

    def get_pull_requests(self, page_start: int, page_end: int) -> List[dict]:
        data_all = []

        url = '{}/repos/BrandEmbassy/platform-backend/pulls?state=all&page={}'.format(self.API_URL, page_start)

        current_page = page_start

        total_pages_number = None

        while current_page <= page_end:
            if total_pages_number is None:
                print('Downloading', end='\r')
            else:
                print('Downloading page {} / {}'.format(current_page, min(total_pages_number, page_end)), end='\r')
            sys.stdout.flush()

            response = self.make_request_to_github(url)

            links = self.parse_links(response.headers.get('Link'))
            if total_pages_number is None and 'last' in links:
                total_pages_number = links['last']['page']

            data_for_page = self.append_detailed_data_about_pull_requests(json.loads(response.read()))
            data_all = data_all + data_for_page

            if 'next' in links:
                url = links['next']['link']
                current_page = current_page + 1
            else:
                break

        print('                                                              ')
        sys.stdout.flush()

        return data_all

    def make_request_to_github(self, url: str) -> HTTPResponse:
        password_manager = urllib.request.HTTPPasswordMgrWithPriorAuth()
        password_manager.add_password(None, url, self.username, self.token, is_authenticated=True)

        request_opener = self.create_request_opener(password_manager)
        request = urllib.request.Request(url=url, method='GET')

        return request_opener.open(request)

    def append_detailed_data_about_pull_requests(self, pull_requests_data: List[dict]) -> List[dict]:
        detailed_pull_requests_data = []

        pull_requests_data_queue = queue.Queue()

        loop = asyncio.get_event_loop()
        futures = []
        executor = ThreadPoolExecutor(max_workers=len(pull_requests_data))

        for pull_request_data in pull_requests_data:
            futures.append(loop.run_in_executor(executor, self.finalize_pull_request_data_and_write_to_queue,
                                                pull_request_data, pull_requests_data_queue))

        loop.run_until_complete(asyncio.wait(futures, loop=loop, return_when=asyncio.ALL_COMPLETED))

        while True:
            try:
                pull_request_data = pull_requests_data_queue.get_nowait()
                detailed_pull_requests_data.append(pull_request_data)
            except queue.Empty:
                break

        return detailed_pull_requests_data

    def finalize_pull_request_data_and_write_to_queue(self, pull_request_data: dict,
                                                      pull_requests_data_queue: queue.Queue) -> None:
        pull_request_data_final = pull_request_data
        pull_request_data_final['detail_info'] = self.get_detail_data_from_pull_request(pull_request_data)

        pull_requests_data_queue.put(pull_request_data_final)

    def get_detail_data_from_pull_request(self, pull_request_data: dict) -> dict:
        response = self.make_request_to_github(pull_request_data['url'])
        pull_request_detail = json.loads(response.read())

        return pull_request_detail

    @staticmethod
    def parse_links(links_from_header: str) -> dict:
        links = {}

        search_data = re.findall(r'<([^>]*(page=([0-9]+))[^>]*)>; rel=\"([\w]+)\"', links_from_header, re.MULTILINE)

        for search_data_item in search_data:
            links[search_data_item[3]] = {
                'link': search_data_item[0],
                'page': int(search_data_item[2]),
            }

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
