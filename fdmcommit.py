import requests
import os
import logging.handlers
import urllib3
from webexteamssdk import WebexTeamsAPI

# setup log class
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# setup rotating logs
file_handler = logging.handlers.RotatingFileHandler('commit.log', maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.DEBUG)
# setup console logging
console_stream_handler = logging.StreamHandler()
console_stream_handler.setLevel(logging.DEBUG)
# setup time date formatting
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_stream_handler.setFormatter(formatter)
# attach file and console logging to the log class
log.addHandler(file_handler)
log.addHandler(console_stream_handler)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FDM:
    token = None
    teams = WebexTeamsAPI()  # TODO: add exception handling

    def __repr__(self):
        return f'{self.__class__.__name__}'

    def __init__(self):
        log.debug(f'Initializing {FDM}')
        self.user = os.getenv('USER')
        self.pwd = os.getenv('PASS')
        self.api = 'https://192.168.128.1/api/fdm/latest'  # TODO: make host a variable
        self.headers = {'Content-Type': 'application/json'}
        if self.token is None:
            self.get_token()  # TODO: check for token expiration

    def get_token(self):
        """
        Log into the FDM API with admin credentials stored in environment variables and get a token for subsequent
        requests.  Add the Bearer token to the Authorization header.

        :return: returns the current token for testing purposes.
        """
        payload = f'''{{
    "grant_type": "password",
    "desired_expires_in": 1800,
    "desired_refresh_expires_in":2400,
    "desired_refresh_count": 0,
    "username": "{self.user}",
    "password": "{self.pwd}"
}}'''
        response = requests.post(self.api + '/fdm/token', headers=self.headers, data=payload, verify=False).json()
        FDM.token = response['access_token']  # This token is stored in the class for use by all instances
        self.headers['Authorization'] = f'Bearer {self.token}'
        return response['access_token']

    def inspect_pending_changes(self):
        response = requests.get(self.api + '/operational/pendingchanges', headers=self.headers, data=None,
                                verify=False).json()
        if False in {item['entityType'] == 'sruversion' for item in response['items']}:
            log.debug('non-SRU items in pendingchanges. Exiting.')
            log.debug({item['entityType'] == 'sruversion' for item in response['items']})
            log.debug((response['items']))
            self.teams.messages.create(toPersonEmail=os.getenv('EMAIL'),
                                      text='non-SRU items in pendingchanges. Exiting.')
            raise Exception('non-SRU items in pendingchanges')
        elif True in {item['entityType'] == 'sruversion' for item in response['items']}:
            try:
                response = requests.post(self.api + '/operational/deploy', headers=self.headers, data=None,
                                         verify=False)
                self.teams.messages.create(toPersonEmail=os.getenv('EMAIL'),
                                          text='successful deployment')
                return
            except:
                self.teams.messages.create(toPersonEmail=os.getenv('EMAIL'),
                                          text='failed to deploy')
                raise Exception(f"{self} - failed to deploy - {response}")
        elif len({item['entityType'] == 'sruversion' for item in response['items']}) == 0:
            log.debug('no changes to deploy')
            self.teams.messages.create(toPersonEmail=os.getenv('EMAIL'),
                                      text='no changes to deploy')
            return
        else:
            self.teams.messages.create(toPersonEmail=os.getenv('EMAIL'),
                                      text='non-True/False/zero in pendingchanges')
            raise Exception(f'non-True/False/zero in pendingchanges - {response}')


if __name__ == '__main__':
    fdm = FDM()
    print(fdm.inspect_pending_changes())
