"""
Example on How to upload sensor's data to OpenPlantbook API.
This example uses fake generated sensor data of 4 measurements related to a Plant
The example uses json_timeseries library https://pypi.org/project/json-timeseries/
In the example, Plantbook Client creds are set from env variables
"""
import json
import os

import numpy as np
import pandas as pd
import requests
from json_timeseries import TimeSeries, TsRecord, JtsDocument


# depends on PlantBookAPI.py in the same directory
# from ..PlantBookAPI.PlantBookAPI import PlantBookAPI
# Just copy/pasted this class from another example - it's ugly but will refactor using https://pypi.org/project/pyopenplantbook/ later
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
        self.session = None

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

    def post(self, endpoint, **kwargs):
        """
        Make a POST request to the PlantBook API.
        :param endpoint: The API endpoint to query.
        :param kwargs: The query parameters for the API endpoint.
        :return: The API response.
        """
        url = f"{PlantBookAPI.BASE_URL}{endpoint}"
        return self.session.post(url, **kwargs)


def upload_sensor_data():
    """
    Upload sensor-data
    """

    NUMBER_OF_PERIODS = 2

    # generate fake data for this example
    pid = "abelia chinensis"
    location_country = "Australia"

    dti = pd.date_range(pd.Timestamp.now(tz="Australia/Sydney"), periods=NUMBER_OF_PERIODS, freq="15min")

    # generate fake values - 4 columns to provide 4 values for the following measurements: temp, soil_moist, soil_ec, light_lux
    df = pd.DataFrame(np.random.default_rng().uniform(100, 1000, (NUMBER_OF_PERIODS, 4)), index=dti).astype(int)

    custom_id = "Sample instance of " + pid

    # Setting required parameters
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]

    client = PlantBookAPI(client_id, client_secret)
    client.login()

    # *** Create Plant instance
    payload = {
        "custom_id": custom_id,
        "pid": pid,
        "location_country": location_country
    }

    response = client.post("/sensor-data/instance", json=payload)

    # *** Upload data
    instance_id = response.json().get('id')

    # Create timeseries for every measurement
    temp = TimeSeries(identifier=instance_id, name="temp")
    soil_moist = TimeSeries(identifier=instance_id, name="soil_moist")
    soil_ec = TimeSeries(identifier=instance_id, name="soil_ec")
    light_lux = TimeSeries(identifier=instance_id, name="light_lux")

    # parse generated fake data creating Record in corresponding TimeSeries
    # "ts" here is TimeStamp
    for ts, values in df.iterrows():
        temp.insert(TsRecord(ts, values[0]))
        soil_moist.insert(TsRecord(ts, values[1]))
        soil_ec.insert(TsRecord(ts, values[2]))
        light_lux.insert(TsRecord(ts, values[3]))

    jts_doc = JtsDocument([temp, soil_moist, soil_ec, light_lux])

    # Setting dry_run=True as it is not real data. Removing the parameter will upload real-data into OPB database
    response = client.post("/sensor-data/upload" + "?dry_run=True", json=json.loads(jts_doc.toJSON()))

    print(response)


upload_sensor_data()
