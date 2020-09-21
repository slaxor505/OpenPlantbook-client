# OpenPlantbook-client
This is repository for Open Plantbook API sample clients.

## Requirements
In order to use this API you need to login to Open Plantbook web UI at https://open.plantbook.io and generate API credentials. The credentials are client_id and client_secret. API authentication implements OAuth2 standard Client Credentials Grant flow.

## API Release notes:

### version 1.0
Breaking changes in comparison with 1.0-RC:
- Removed api/v1/plant/detail/{id}/ endpoint
- Removed "id" from responses
- Now to get plant details use api/v1/plant/detail/{pid} endpoint.

## Client Release notes:

### version 1.0
- Updated Postman collection:
    - built-in variables for easier use (See variables specific to the Collection)
    - "Get token" call now extracts and updates {{access_token}} value automatically (no need to copy/paste)
- Added Python client by @Olen (https://github.com/Olen). Thanks and Kudos! The client is a step for Home-assistant.io integration and this is why it is a bit overcomplicated.  

## Usage
The easiest way to get familiar with API is to use Browsable API within Web UI. The link can be found within Docs section.
Alternatively, you can use excellent and easy tool - Postman. Postman collection can be found in corresponding folder of this repository. You need to install free Postman API tool: https://www.postman.com/ then import the collection.

### Below is a manual walk through using CURL.

1. Get API credentials from Web UI.

2. Get access token using API credentials.
```
curl --request POST 'https://open.plantbook.io/api/v1/token/' \
--form 'grant_type=client_credentials' \
--form 'client_id=string_client_id_from_UI' \
--form 'client_secret=string_client_secret_from_UI'
```
Response will be:
```
{
    "access_token": "token_string",
    "expires_in": 2629800,
    "token_type": "Bearer",
    "scope": "read"
}
```
This is token to access API. It will expire in 2629800 seconds = 1 month. It is ok to get a new token everytime.
We will need "token_string" at next step.

3. Make a Plant Search API call with 'Bearer Token' HTTP header:
Query parameter ?alias=<search string> is required.
```
curl --request GET 'https://open.plantbook.io/api/v1/plant/search?alias=acanthus%20ilicifolius' \
--header 'Authorization: Bearer token_string'
```
From the response, you can to get Plant Id (pid) in order to get the plant details.
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "pid": "acanthus ilicifolius",
            "display_pid": "Acanthus ilicifolius",
            "alias": "acanthus ilicifolius"
        },
        {
            "pid": "acanthus spinosus",
            "display_pid": "Acanthus spinosus",
            "alias": "acanthus ilicifolius"
        }
    ]
}
```
4.  From previous step, take "pid" value of the desired plant and get the plant details with Bearer Token. 

```
curl --request GET 'https://open.plantbook.io/api/v1/plant/detail/acanthus ilicifolius/' \
--header 'Authorization: Bearer token_string'
```
```
{
    "pid": "acanthus ilicifolius",
    "display_pid": "Acanthus ilicifolius",
    "alias": "acanthus ilicifolius",
    "max_light_mmol": 2500,
    "min_light_mmol": 1200,
    "max_light_lux": 6000,
    "min_light_lux": 1500,
    "max_temp": 32,
    "min_temp": 10,
    "max_env_humid": 80,
    "min_env_humid": 30,
    "max_soil_moist": 60,
    "min_soil_moist": 15,
    "max_soil_ec": 2000,
    "min_soil_ec": 350
}
```
