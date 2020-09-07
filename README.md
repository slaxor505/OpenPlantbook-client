# OpenPlantbook-client
This is repository for Open Plantbook API sample clients.

## Requirements
In order to use this API you need to login to Open Plantbook web UI at https://open.plantbook.io and generate API credentials. The credentials are client_id and client_secret. API authentication implements OAuth2 standard Client Credentials Grant flow.

## Usage
The easies way to get familiar with API is to use Browsable API within Web UI. The link can be found within Docs section.
Alternatively, you can use excellent easy tool - Postman. Postman collection can be found in corresponding folder of this repository. You need to install free Postman API tool: https://www.postman.com/ and then import the collection.

### Below is an manual walk through using CURL.

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
We will need "token_string" on next step.

3. Make a Plant Search API call with 'Bearer Token' HTTP header:
Query parameter ?alias=<search string> is required.
```
curl --request GET 'https://open.plantbook.io/api/v1/plant/search?alias=acanthus ilicifolius' \
--header 'Authorization: Bearer SqtIGQGIINB5KXZuabyTwhTGSyMoUmgkq5t1TBGI'
```
In the response you will be able to get Plants Id in order to get details.
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 38,
            "alias": "acanthus ilicifolius",
            "display_pid": "Acanthus ilicifolius"
        },
        {
            "id": 40,
            "alias": "acanthus ilicifolius",
            "display_pid": "Acanthus spinosus"
        }
    ]
}
```
4.  Get details about plant again using Bearer Token:
```
curl --request GET 'https://open.plantbook.io/api/v1/plant/detail/68' \
--header 'Authorization: Bearer SqtIGQGIINB5KXZuabyTwhTGSyMoUmgkq5t1TBGI'
```
```
{
    "id": 68,
    "pid": "acer sieboldianum",
    "display_pid": "Acer sieboldianum",
    "alias": "acer sieboldianum",
    "max_light_mmol": 7200,
    "min_light_mmol": 3000,
    "max_light_lux": 75000,
    "min_light_lux": 2800,
    "max_temp": 35,
    "min_temp": 5,
    "max_env_humid": 80,
    "min_env_humid": 30,
    "max_soil_moist": 60,
    "min_soil_moist": 15,
    "max_soil_ec": 2000,
    "min_soil_ec": 350
} 
```
Known limitations:
Potential issue at the moment is that "id" is not reliable and can be changed as it is managed by DB internally. Hence, if it cannot be used to  reliably identify a particular plant. Therefore, search is required to get this "id" before getting plant details. 
I will be working on more reliable ID to get plant details. Possible it will be  HASH of plant name or plain "pid" field.
