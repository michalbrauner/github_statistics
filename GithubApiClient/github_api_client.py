import json
import ssl
import urllib.request
from http import cookiejar


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
        url = '{}/repos/BrandEmbassy/platform-backend/pulls?state=all'.format(self.API_URL)

        password_manager = urllib.request.HTTPPasswordMgrWithPriorAuth()
        password_manager.add_password(None, url, self.username, self.token, is_authenticated=True)

        request_opener = self.create_request_opener(password_manager)
        request = urllib.request.Request(url=url, method='GET')
        response = request_opener.open(request)

        return json.loads(response.read())

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
