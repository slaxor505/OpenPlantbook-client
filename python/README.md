# Usage
* Get client_id and secret from the Openplantbook API: https://open.plantbook.io/docs.html
* Download the files
* Rename config.yaml.dist to config.yaml
* Insert client_id and secret in the config file
* Install dependencies (see requirements.txt)

## search.py
- Search for a plant alias. Lists all hits from the API


```
$ python search.py capsicum
+----------------------------------------+----------------------------------------+-------------------------------------+
| PID                                    | Display PID                            | Alias                               |
|----------------------------------------+----------------------------------------+-------------------------------------|
| capsicum annuum                        | Capsicum annuum                        | capsicum annuum                     |
| capsicum favorit purple red 'gt58'     | Capsicum Favorit Purple Red 'GT58'     | capsicum annuum                     |
| capsicum favorit yellow                | Capsicum Favorit Yellow                | capsicum annuum                     |
| capsicum favorit yellow red 'gt57'     | Capsicum Favorit Yellow Red 'GT57'     | capsicum annuum                     |
| capsicum mambo orange                  | Capsicum Mambo orange                  | capsicum annuum                     |
 (...)
| solanum pseudocapsicum 'thurino light' | Solanum pseudocapsicum 'Thurino Light' | solanum pseudocapsicum              |
+----------------------------------------+----------------------------------------+-------------------------------------+
40 plants found
```

## plant.py
- List all details for a single plant.  
- Ensure that you wrap names with spaces in `""` and that you include the complete pid - with any `'` etc
```
$ python plant.py "capsicum favorit purple red 'gt58'"
+----------------+------------------------------------+
| Key            | Value                              |
|----------------+------------------------------------|
| pid            | capsicum favorit purple red 'gt58' |
| display_pid    | Capsicum Favorit Purple Red 'GT58' |
| alias          | capsicum annuum                    |
| max_light_mmol | 12000                              |
| min_light_mmol | 4400                               |
| max_light_lux  | 95000                              |
| min_light_lux  | 3000                               |
| max_temp       | 35                                 |
| min_temp       | 10                                 |
| max_env_humid  | 80                                 |
| min_env_humid  | 30                                 |
| max_soil_moist | 65                                 |
| min_soil_moist | 20                                 |
| max_soil_ec    | 2000                               |
| min_soil_ec    | 150                                |
+----------------+------------------------------------+

```

