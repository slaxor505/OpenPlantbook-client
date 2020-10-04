
import requests
import yaml
import logging
import sys
from tabulate import tabulate


logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

def get_plantbook(alias, token):
    """ Searches plantbook and list results """
    url = "https://open.plantbook.io/api/v1/plant/search?limit=1000&alias={}".format(alias)
    headers = {"Authorization": "Bearer {}".format(token)}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        _LOGGER.error("Timeout connecting to {}".format(url))
        return
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        _LOGGER.error("Too many redirects connecting to {}".format(url))
        return
    except requests.exceptions.HTTPError as err:
        _LOGGER.error(err)
        return
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        _LOGGER.error(err)
        return
    res = result.json()
    _LOGGER.debug("Fetched data from {}:".format(url))
    _LOGGER.debug(res)
    print(tabulate(res['results'], headers={'pid': 'PID', 'display_pid': 'Display PID', 'alias': 'Alias'}, tablefmt="psql"))
    print("{} plants found".format(len(res['results'])))


def get_plantbook_token(client_id, secret):
    """ Gets the token from the openplantbook API """
    url =  'https://open.plantbook.io/api/v1/token/'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': secret
    }
    try:
        result = requests.post(url, data = data)
        result.raise_for_status()
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        _LOGGER.error("Timeout connecting to {}".format(url))
        return
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        _LOGGER.error("Too many redirects connecting to {}".format(url))
        return
    except requests.exceptions.HTTPError as err:
        _LOGGER.error(err)
        return
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        _LOGGER.error(err)
        return
    token = result.json().get('access_token')
    _LOGGER.debug("Got token {} from {}".format(token, url))
    return token


with open('config.yaml') as file:
    try:
        config = yaml.load(file, Loader=yaml.FullLoader)
    except Exception:
        print("Unable to open 'config.yaml'")
        sys.exit()

if len(sys.argv) < 2:
    print("Usage: {} <name>".format(sys.argv[0]))
    sys.exit(1)

searchstring = sys.argv[1]

if 'openplantbook' in config:
    token = get_plantbook_token(config['openplantbook']['client_id'], config['openplantbook']['secret'])
    get_plantbook(searchstring, token)
