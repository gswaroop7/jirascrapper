from common import Logging
from common import config as cfg
import requests

__all__ = ['JiraConnect']

class JiraConnect(Logging):
    def __init__(self, userid, token, **kwargs):
        super().__init__(**kwargs)
        self.session = self._create_session(userid, token)
        self.base_url = cfg.BASE

    @staticmethod
    def _create_session(userid, token):
        session = requests.Session()
        session.auth = (userid, token)
        return session

    def get(self, request_string, params=None):
        try:
            request_string = f"{self.base_url}{request_string}"
            self.logger.debug(f"Fetching details from Jira using url: {request_string}")
            resp = self.session.get(request_string, params=params, verify=True, proxies={'http': None, 'https': None})
            #self.logger.debug(f"Headers being used are : {resp.headers}")
            self.logger.debug(f"Jira response code: {resp.status_code}")
            return self._analyse_jira_response(resp)
        except Exception as e:
            return '',str(e)

    @staticmethod
    def _analyse_jira_response(resp):
        if resp.status_code != requests.codes.ok:
            return '',f'{resp.status_code} {resp.text}'
        else:
            return f'{resp.text}',''