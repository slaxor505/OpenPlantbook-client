"""
This script uses the Open PlantBook API to query information about plants.

Language: Python
PlantBook API (https://open.plantbook.io/)
"""

import os
import json
import requests
import urllib.parse



class PlantBookAPI(object):
    BASE_URL = "https://open.plantbook.io/api/v1"

    def __init__(self, client_id, client_secret):
        """
        Initialize the PlantBookAPI client with client_id and client_secret.
        :param client_id: The client ID for the PlantBook API.
        :param client_secret: The client secret for the PlantBook API.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.logged_in = False

        token = os.environ.get("PLANTBOOK_ACCESS_TOKEN", None)
        if token is not None:
            self._create_session(token)


    def login(self):
        """
        Log in to the PlantBook API and store the access_token.
        :return: True if logged in successfully, otherwise raises an exception.
        """
        if self.logged_in:
            return True

        post_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        r = requests.post(f"{PlantBookAPI.BASE_URL}/token/", data=post_data)
        if r.status_code != 200:
            raise Exception(
                f"Unable to generate access_token (HTTP {r.status_code})")

        self._create_session(r.json()["access_token"])
        return True


    def _create_session(self, token):
        """
        Create a session with the PlantBook API using the access_token.
        :param token: The access_token for the PlantBook API.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f"Bearer {token}"
        })
        self.logged_in = True

    # @endpoint string - The part of the path that comes after /api/v1.
    #     e.g. https://open.plantbook.io/api/v1/plant/search would have endpoint = "/plant/search"
    # @kwargs - A list of arguments to pass as ?kwarg1=val1&kwarg2=val2.
    #     e.g. https://open.plantbook.io/api/v1/plant/search?alias=acer&limit=10&offset=20 would
    #     have the same endpoint as above and be called like so:
    #     client.get("/plant/search", alias=acer, limit=1, offset=20)
    #
    # API docs for all endpoints and arguments:
    # https://documenter.getpostman.com/view/12627470/TVsxBRjD#intro
    
    
    def get(self, endpoint, **kwargs):
        """
        Make a GET request to the PlantBook API.
        :param endpoint: The API endpoint to query.
        :param kwargs: The query parameters for the API endpoint.
        :return: The API response.
        """
        url = f"{PlantBookAPI.BASE_URL}{endpoint}"
        return self.session.get(url, params=kwargs)

# Uncomment to test.
client = PlantBookAPI(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])
# print(json.dumps(client.get("/plant/search", alias="acer", limit=5).json()))

