import flow_utils
import constants
from oauth2client import client
from handler import request_handler

class OAuthChecker(request_handler.Request):

    @request_handler.json
    def getAuthURI(self):
        url = self.request.uri.split(self.request.path)[0] + '/'
        return {'auth_uri': flow_utils.getFlow(url).step1_get_authorize_url()}

    def verify(self):
        credentials = getCredentials(self.request.cookies)
        if credentials is None or credentials.access_token_expired:
            return False
        return True

    def createCookie(self):
        auth_code = self.param('code')
        uri = self.request.uri.split(self.request.path)[0] + '/'
        flow = flow_utils.getFlow(uri)
        credentials = flow.step2_exchange(auth_code)
        self.response.set_cookie(constants.COOKIE_NAME, credentials.to_json(),  path='/')
        return uri

def getCredentials(cookies):
    try:
        return client.OAuth2Credentials.from_json(read_valid_cookie(cookies))
    except ValueError:
        return None

def read_valid_cookie(cookies):
    if constants.COOKIE_NAME in cookies:
        text = cookies[constants.COOKIE_NAME]
        return str(text)

    return None
