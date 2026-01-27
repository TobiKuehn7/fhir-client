import requests
from requests.auth import AuthBase

from fhir_client.auth import FhirAuth


class FhirClient:
    def __init__(self, url: str, auth:AuthBase = None):
        """
        Initializes the FHIR client.

        :param url: URL of the FHIR server.
        :param auth: Dictionary containing 'username' and 'password' for Basic Authentication.
        """
        self.url = url
        self.auth = auth

    def get(self, resource: str, **params):
        """
        Get a FHIR resource from the server.

        :param resource: The resource to retrieve (e.g., "Patient/123").
        :return: Response from the server.
        """
        if self.auth:
            response = requests.get(f"{self.url}/{resource}", auth=self.auth, params=params)
        else:
            response = requests.get(f"{self.url}/{resource}", params=params)
        return response.json()

    def post(self, resource: str, data: dict, **params):
        """
        Add a new resource to the FHIR server.

        :param resource: The resource to post to (e.g., "Patient").
        :param data: The data to post (in JSON format).
        :return: Response from the server.
        """
        if self.auth:
            response = requests.post(f"{self.url}/{resource}", json=data, auth=self.auth, params=params)
        else:
            response = requests.post(f"{self.url}/{resource}", json=data, params=params)
        return response.json()

    def put(self, resource: str, data: dict, **params):
        """
        Update an existing resource on the FHIR server.

        :param resource: The resource to update (e.g., "Patient/123").
        :param data: The updated data to put.
        :return: Response from the server.
        """
        if self.auth:
            response = requests.put(f"{self.url}/{resource}", json=data, auth=self.auth, params=params)
        else:
            response = requests.put(f"{self.url}/{resource}", json=data, params=params)
        return response.json()

    def delete(self, resource: str, **params):
        """
        Delete a resource from the FHIR server.

        :param resource: The resource to delete (e.g., "Patient/123").
        :return: Response from the server.
        """
        if self.auth:
            response = requests.delete(f"{self.url}/{resource}", auth=self.auth, params=params)
        else:
            response = requests.delete(f"{self.url}/{resource}", params=params)
        return response.status_code
