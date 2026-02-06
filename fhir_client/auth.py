import requests
from requests.auth import AuthBase, HTTPBasicAuth


class FhirAuth:
    def __init__(self, auth_type:str=None):
        self.type = auth_type
        self.auth = None

    def set_basic_auth(self, username, password) -> AuthBase:
        self.type = 'basic'
        self.auth = HTTPBasicAuth(username, password)
        return self.auth

    def set_o_auth(self, auth_url, client_id, client_secret) -> AuthBase:
        self.type = 'oauth'
        self.auth = HTTPOAuth2Auth(auth_url, client_id, client_secret)
        return self.auth

    def get_auth_type(self):
        return self.type

class HTTPOAuth2Auth(AuthBase):
    """Attaches Bearer Token from Auth URL to the given Request object."""

    def __init__(self, auth_url, client_id, client_secret, retries:int=3):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret

        # set retries
        self.retries = retries

    def __eq__(self, other):
        return all(
            [
                self.auth_url == getattr(other, "auth_url", None),
                self.client_id == getattr(other, "client_id", None),
                self.client_secret == getattr(other, "client_secret", None),
            ]
        )

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        tries = 0

        while tries < self.retries:
            try:
                body = f'client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials'
                response = requests.post(self.auth_url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                access_token = response.json()["access_token"]
                r.headers["Authorization"] = f'Bearer {access_token}'
                continue
            except Exception as e:
                print(e)
                tries += 1
                if tries >= self.retries:
                    raise e

        return r