import requests
from requests.auth import AuthBase


class FhirClient:
    total = None
    previous = None
    self = None
    next = None

    def __init__(self, url:str, auth:AuthBase=None, headers:dict=None, timeout:float=None, retries:int=None):
        """
        Initializes the FHIR client.

        :param url: URL of the FHIR server.
        :param auth: Dictionary containing 'username' and 'password' for Basic Authentication.
        :param headers: Dictionary containing 'content-type' or similar parameters. Default: 'application/fhir+json'
        :param timeout: Timeout in seconds. Default: 10
        :param retries: Number of retries. Default: 3
        """
        self.url = url
        self.auth = auth
        if headers is None:
            self.headers = {'Content-Type': 'application/fhir+json'}
        if timeout is None:
            self.timeout = 10
        if retries is None:
            self.retries = 3

    def _set_links(self, links:list):
        """
        Resets all links and sets all existing links.

        :param links: List of FHIR links.
        """
        self.previous = None
        self.self = None
        self.next = None

        for link in links:
            if link['relation'] == 'self':
                self.self = link['url']
            if link['relation'] == 'next':
                self.next = link['url']
            if link['relation'] == 'previous':
                self.previous = link['url']

    def get(self, resource: str, **params):
        """
        Get a FHIR resource from the server.

        :param resource: The resource to retrieve (e.g., "Patient/123").
        :return: Response from the server.
        """
        if self.auth:
            response = requests.get(f"{self.url}/{resource}", auth=self.auth, params=params, headers=self.headers)
        else:
            response = requests.get(f"{self.url}/{resource}", params=params, headers=self.headers)

        json_response = response.json()
        if 'total' in json_response:
            self.total = json_response['total']

        if 'link' in json_response:
            self._set_links(json_response['link'])

        return json_response

    def post(self, resource: str, data: dict, **params):
        """
        Add a new resource to the FHIR server.

        :param resource: The resource to post to (e.g., "Patient").
        :param data: The data to post (in JSON format).
        :return: Response from the server.
        """
        if self.auth:
            response = requests.post(f"{self.url}/{resource}", json=data, auth=self.auth, params=params, headers=self.headers)
        else:
            response = requests.post(f"{self.url}/{resource}", json=data, params=params, headers=self.headers)

        json_response = response.json()
        if 'total' in json_response:
            self.total = json_response['total']

        if 'link' in json_response:
            self._set_links(json_response['link'])

        return json_response

    def put(self, resource: str, data: dict, **params):
        """
        Update an existing resource on the FHIR server.

        :param resource: The resource to update (e.g., "Patient/123").
        :param data: The updated data to put.
        :return: Response from the server.
        """
        if self.auth:
            response = requests.put(f"{self.url}/{resource}", json=data, auth=self.auth, params=params, headers=self.headers)
        else:
            response = requests.put(f"{self.url}/{resource}", json=data, params=params, headers=self.headers)

        json_response = response.json()
        if 'total' in json_response:
            self.total = json_response['total']

        if 'link' in json_response:
            self._set_links(json_response['link'])

        return json_response

    def delete(self, resource: str, **params):
        """
        Delete a resource from the FHIR server.

        :param resource: The resource to delete (e.g., "Patient/123").
        :return: Response from the server.
        """
        if self.auth:
            response = requests.delete(f"{self.url}/{resource}", auth=self.auth, params=params, headers=self.headers)
        else:
            response = requests.delete(f"{self.url}/{resource}", params=params, headers=self.headers)

        json_response = response.json()
        if 'total' in json_response:
            self.total = json_response['total']

        if 'link' in json_response:
            self._set_links(json_response['link'])

        return json_response

    def has_next(self):
        if self.next is not None:
            return True
        else:
            return False

    def has_self(self):
        if self.self is not None:
            return True
        else:
            return False

    def has_previous(self):
        if self.previous is not None:
            return True
        else:
            return False
