import requests
import yaml
import logging
import sys

_LOGGER = logging.getLogger(__name__)

DEFAULT_MIN_MOISTURE = 20
DEFAULT_MAX_MOISTURE = 60
DEFAULT_MIN_CONDUCTIVITY = 500
DEFAULT_MAX_CONDUCTIVITY = 3000
DEFAULT_MIN_TEMPERATURE = 10
DEFAULT_MAX_TEMPERATURE = 30
DEFAULT_MIN_BRIGHTNESS = 1000
DEFAULT_MAX_BRIGHTNESS = 30000

class Plant():

    def __init__(self, name, config, token):
        """Initialize the Plant component."""
        self._config = config
        self._name = name
        self._species = self._config.get('species')
        self._plantbook_token = token
        if self._species:
            self.get_plantbook_data()
        else:
            self.populate_default_data()

    def get_plantbook_data(self):
        """ Gets information about the plant from the openplantbook API """
        if not self._plantbook_token:
            return
        url = "https://open.plantbook.io/api/v1/plant/detail/{}".format(self._species)
        headers = {"Authorization": "Bearer {}".format(self._plantbook_token)}
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
        self._name = res['display_pid']
        self._set_conf_value('min_temperature', res['min_temp'])
        self._set_conf_value('max_temperature', res['max_temp'])
        self._set_conf_value('min_moisture', res['min_soil_moist'])
        self._set_conf_value('max_moisture', res['max_soil_moist'])
        self._set_conf_value('min_conductivity', res['min_soil_ec'])
        self._set_conf_value('max_conductivity', res['max_soil_ec'])
        self._set_conf_value('min_brightness', res['min_light_lux'])
        self._set_conf_value('max_brightness', res['max_light_lux'])


    def populate_default_data(self):
        """ Adds the default min/max-values if no plantbook config is present """
        self._set_conf_value('min_temperature', DEFAULT_MIN_TEMPERATURE)
        self._set_conf_value('max_temperature', DEFAULT_MAX_TEMPERATURE)
        self._set_conf_value('min_moisture', DEFAULT_MIN_TEMPERATURE)
        self._set_conf_value('max_moisture', DEFAULT_MAX_TEMPERATURE)
        self._set_conf_value('min_conductivity', DEFAULT_MIN_CONDUCTIVITY)
        self._set_conf_value('max_conductivity', DEFAULT_MAX_CONDUCTIVITY)
        self._set_conf_value('min_brightness', DEFAULT_MIN_BRIGHTNESS)
        self._set_conf_value('max_brightness', DEFAULT_MAX_BRIGHTNESS)


    def _set_conf_value(self, var, val):
        """ Ensures that values explicitly set in the config is not overwritten """
        if var not in self._config or self._config[var] is None:
            self._config[var] = val


    @property
    def name(self):
        """Return the name of the plant."""
        return self._name

    @property
    def species(self):
        """Return the species of the plant."""
        return self._species

    @property
    def config(self):
        """Return the full config of the plant."""
        return self._config


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

plants = {}
if 'openplantbook' in config:
    token = get_plantbook_token(config['openplantbook']['client_id'], config['openplantbook']['secret'])

for plant_name, plant_config in config.items():
    if plant_name != 'openplantbook':
        plants[plant_name] = Plant(plant_name, plant_config, token)

        print(plants[plant_name].name)
        print(plants[plant_name].config)
