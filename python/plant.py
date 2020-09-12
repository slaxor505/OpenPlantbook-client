import requests
import yaml



class Plant():
    DEFAULT_MIN_MOISTURE = 20
    DEFAULT_MAX_MOISTURE = 60
    DEFAULT_MIN_CONDUCTIVITY = 500
    DEFAULT_MAX_CONDUCTIVITY = 3000
    DEFAULT_MIN_TEMPERATURE = 10
    DEFAULT_MAX_TEMPERATURE = 30
    DEFAULT_MIN_BRIGHTNESS = 1000
    DEFAULT_MAX_BRIGHTNESS = 30000

    def __init__(self, name, config):
        """Initialize the Plant component."""
        self._config = config
        self._name = name
        self._species = self._config.get('species:')
        self._plantbook_token = None
        if self._config['plantbook_client_id'] and self._config['plantbook_client_secret']:
            self.get_plantbook_data()

    def get_plantbook_data(self):
        if not self._plantbook_token:
            self.get_plantbook_token()
        url = "https://open.plantbook.io/api/v1/plant/detail/{}".format(self._species)
        url = "https://open.plantbook.io/api/v1/plant/detail/5494/"
        headers = {"Authorization": "Bearer {}".format(self._plantbook_token)}
        result = requests.get(url, headers=headers).json()
        self._name = result['display_pid']
        self._config['min_temperature'] = result['min_temp']
        self._config['max_temperature'] = result['max_temp']
        self._config['min_moisture'] = result['min_soil_moist']
        self._config['max_moisture'] = result['max_soil_moist']
        self._config['min_conductivity'] = result['min_soil_ec']
        self._config['max_conductivity'] = result['max_soil_ec']
        self._config['min_brightness'] = result['min_light_lux']
        self._config['max_brightness'] = result['max_light_lux']

    def get_plantbook_token(self):
        url =  'https://open.plantbook.io/api/v1/token/'
        data = {
            'grant_type': 'client_credentials',
            'client_id': self._config['plantbook_client_id'],
            'client_secret': self._config['plantbook_client_secret']
        }
        result = requests.post(url, data = data).json()
        self._plantbook_token = result.get('access_token')

    @property
    def name(self):
        """Return the name of the plant."""
        return self._name

    @property
    def spieces(self):
        """Return the name of the plant."""
        return self._spieces

    @property
    def config(self):
        return self._config

with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


plants = {}
for plant_name, plant_config in config.items():
    plants[plant_name] = Plant(plant_name, plant_config)

    print(plants[plant_name].name)
    print(plants[plant_name].config)
