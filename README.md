# OpenPlantbook-client
This is a repository for Open Plantbook Cloud and Client release notes, documentation and sample clients.

## Requirements
To use this API you need to log in to Open Plantbook web UI at https://open.plantbook.io and generate API credentials. The credentials are client_id and client_secret. API authentication implements OAuth2 standard Client Credentials Grant flow.

## Documentation
- [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD)
- [Web UI documentation](https://github.com/slaxor505/OpenPlantbook-client/wiki)

## Open Plantbook Cloud release notes:

### **COMING BREAKING CHANGE:** 
API THROTTLING WILL BE ENABLED from 1 November 2025.
API requests will be capped to 200 requests per user per day. This is only to prevent API usage abuse by bots and crawlers and preserve the service for other users.
If you need more requests for any reason, please contact me.

### release 202509 (8 September 2025)
- New feature: International Common Names for both Public and User-plants
- UI: Add Common Name forms have autocomplete suggestions to avoid typos and duplicates
- UI: Browse Plants page now displays additional Common Names
- UI: Added Plant's Origin field
- UI: Updated Plant operations and Plant details pages to group fields by category
- Both API and UI Plant Search now search across multilingual Common Names
- Minor UI fixes and improvements
- Security updates

### release 202502 (17 February 2025)
- Fixed issue when user can't delete User-plant if it has been copied by other users
- Framework and libraries updates

### release 202501 (8 January 2025)
- Added ability to upload plant images in UI. Now you can upload images for your User-plants.
- Added display_pid validation in UI and API
- Internal updates
- Framework and libraries updates

### release 202412 (11 December 2024)
- Completely rebuild Public and User Plants Operations UI and Backend. Now operations are just simple and straight forward Edit & Copy. [Read more](https://github.com/slaxor505/OpenPlantbook-client/wiki/Plants-operations)
- New Copy operation for own User-plants 
- Browse User-plants now includes users' Copied/Cloned plants
- Added auto-generated PID field to all Plant Operation forms for convenience
- Updated text labels in Plant Operation forms
- Changing "Scientific name" creates a new User-plant
- Don't allow to modify display_pid when Edit plants
- Internal updates
- Changed license for this repository to MIT

### release 202410 (27 October 2024)
- Added PID to Plant Detail form
- Fixed issue where empty field in JSON time series cause upload error. Now empty values are ignored since they are optional as per JSON Timeseries spec.
- Adjusted some text messages in UI
- Security updates

### release 20240605 (5 June 2024)
- Major Web framework upgrade
- Components and libraries updated to the latest

### release 20240601 (1 June 2024)
- Sensor page now display live World Sensor Map where plants and its sensors can be mapped to countries
- Removed Facebook login due to its restrict policies
- Internal maintenance improvements

### April 2024
Introducing [OpenPlantbook Dotnet library](https://github.com/denxorz/OpenPlantbook-client-dotnet). 
This library adds support of OpenPlantbook API for DotNet apps.

### release 202401 (3 January 2024)
- Improvements in Sensor-data API and functionality
- Performance improvements for Grafana Dashboard
- Changes location_country to ISO 2 char code including DB model and validation
- Service reliability improvements
- Web framework and libraries updates

### October 2023

Introducing [OpenPlantbook SDK for Python](https://github.com/slaxor505/openplantbook-sdk-py). 
Using this SDK you can easily integrate your Python application with OpenPlantbook without wrestling with OAuth and API calls.

### release 2307 (25 July 2023)
**Release highlights: Ability to browse and use other users' plants and submit request for a missing plant.**

Our users have already created many plants and starting from this release others can benefit from it. If in UI "Browse DB" no plants (Public-plants) have been found then you can search in users' plants as well. In doing so you can then add (by cloning or linking) other users' plants to "My-plants" so they are available for your integrations.
If the plant, you need, is still not found in users' plants, you can submit a request for the missing plant. These requests will help to find the most demanded missing plants, so we or the community can add them later. The plan is to expose these requests to all of our users so the community can help.  

**All changes and new features:**
- New UI Form to see plants' details and their images
- Ability to Browse other users' plants (user-plants)
- Ability to CLONE or LINK other users' plants (user-plants) to My-Plants
- Ability to request missing plant
- UI revamp, better navigation with breadcrumbs
- Security and reliability updates
- Released Python [json_timeseries for Python](https://pypi.org/project/json-timeseries) library. The library supports [JTS spec](https://docs.eagle.io/en/latest/reference/historic/jts.html) and handles time series data using JSON. The library can be used to integrate with OpenPlantbook Sensor-data API. 

**Roadmap**
- Ability to upload plants' pictures in UI
- Allow to search users' plant (user-plants) via API
- Ability to add and see multiple common names of the plants including in different national languages
- Ability to add, modify and see general information about plants in UI and via API
- Ability to specify alternative thresholds for different seasons of the year (summer, winter, etc.)

### release 2302 (18 February 2023)
**Fully functional Sensor-Data UI**
UI is fully wired using Grafana to display Sensor's data.

- Added initial Grafana dashboard for sensor data
- Changed "supported measurements" for Sensor-upload end-point to be the same as rest of API
- Rework to handle internal asynchronous operations
- Internal platform resilience works

### release 2212 (13 December 2022)
**API-key authentication and CORS header**

- Introduced API-key authentication for Plant's "search" and "detail" endpoints including UI to enable it
- Enabled CORS headers for all "plant" endpoints so it is now possible to make calls from front-end with API-key
- Authentication related documentation updated - see [Authentication](https://documenter.getpostman.com/view/12627470/TVsxBRjD#56623c2d-7182-4b70-b31c-5cb8ed7b38c2)

### release 2211 (30 November 2022)
**Introduction of a major new feature**

Ability to share and browse Plants' sensor data. This is completion of phase one. 
The feature will allow users to share their own and see other users plants' sensor data. For example, if you grow Rose in Norway then you will be able to see environment conditions where these Roses are grown around the world. Moreover, you are not limited to the plants you have, and you will be able to see all users plants sensor’s data which Plantbook have been collected. It will include location (a country and perhaps city) where a particular plant grows bundled with its sensor data. The motivation for users to share their plant’s sensor data is you will be able to see others data if you are sharing yours. Displayed information will be anonymous and only include approximate location, sensor data and related plant.
You can start development of your integration now. Sensor-data endpoints documentation [here](https://documenter.getpostman.com/view/12627470/TVsxBRjD#9728f561-a05b-4886-ba29-25722819150c). Any feedback is always welcome.
Next phase is to introduce UI to browse uploaded senor data from around the world. 

API updates and changes (see [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD) for details):
- Introduced 2 new end-points for sensor-data uploading. (see [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD#9728f561-a05b-4886-ba29-25722819150c) for details)
- POTENTIAL BREAKING CHANGE: Partly standardized API error responses to comply with JSON API standard. All new and some existing endpoints use new format now. In next release, all endpoints will use it. It only affects JSON response payload. Error codes are the same. (see [format details](https://drf-standardized-errors.readthedocs.io/en/latest/error_response.html)) 
- Minor bug fixes

UI updates:
- Added Menu and Page-placeholder for "Sensor Data"
- Minor UI improvements

Maintenance:
- Updated web framework and libraries to secure versions.
- Improved internal reliability and manageability

### release 2209 (19 September 2022)
UI updates:
- Added validation when saving a modified Public Plant. User cannot save modified public plant if its no attributes have been modified.
- Added stylised notifications to reflect results of operations
- Added "Category" when creating and modifying plants
- Other minor UI fixes and improvements

API updates and changes (see [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD) for details):
- Plant Search endpoint now returns combined user + public plants result with deduplication.
- Plant Search results now include plant's Category.
- Introduced search selector "userplant" to Plant Search endpoint. Now it is possible to search public and user plants, and get separate (user/public) and combined results.
- Plant Details endpoint returns extra field "'user_plant': True" if resulting plant is user-plant.
- Added "Category" field when creating and modifying plants

Maintenance:
- Updated web framework and libraries to the secure and vulnerabilities free versions.

### release 2205 (25 May 2022):
Now all plant image requests are proxied/cached using CloudFlare servers across the globe so images are fast to download independently on your location on the planet.

### version 1.04 (20 July 2021)
Major UI update. Now Users can:
- Modify existing Public-Plants using "Modify" button in Browse DB.
- Add new Plants using "Add Plant" button in side Menu. Plant is cloned into User-Plant and visible in "My Plants" side menu.
- Modify own User-Plants via "My Plants" side menu.
- The only way to delete User-Plant at the moment is via API DELETE call. UI-based deletion will be available in next release.

The detailed documentation about UI Add/Modify operations is available in [Wiki](https://github.com/slaxor505/OpenPlantbook-client/wiki). 

### version 1.03 (26 December 2020)
Major update:
- Ability to add new and edit existing plants via API calls. (not UI yet)

Now user can update existing plant or create new one. 
There are 2 databases: user specific database (user's context) and main database (public).
- All modifications of plants (new, existing) are only visible for the user who have modified them. Later, moderator can merge these modifications into main public database.
- A modification of an existing plant creates a "shadow" or clone of the plant in the user context. 
- Once a plant has been updated, the user can only see this updated (shadow) version of the plant but not public version of it.
- Newly created plants are only available to the user who created them until a moderator merges them into a main database.
- It is not possible to create plant which already exists in a main DB. It can only be updated with API update call.
- New or updated plants can be deleted from user context.
- Once updated existing plant is deleted from user context (user's version of existing plant), the user can again retrieve a public version of the plant from main database.
  
### version 1.02
- Introduction of Plant images feature. api/v1/plant/detail/ endpoint returns Plant's image URL as image_url JSON string field.
- Web UI is generally available for guests. Guests can search Plant DB but to get API key and plants details Signing in is required.

### version 1.01
- Browse-DB feature in WebUI so it is possible to search plants available in DB.
- Small UI clean-ups

### version 1.0
Breaking changes in comparison with 1.0-RC:
- Removed api/v1/plant/detail/{id}/ endpoint
- Removed "id" from responses
- Now to get plant details use api/v1/plant/detail/{pid} endpoint.

## Open Plantbook API Release notes:

### April 2024
Introducing [OpenPlantbook Dotnet library](https://github.com/denxorz/OpenPlantbook-client-dotnet). 
This library adds support of OpenPlantbook API for DotNet apps.

### version 1.0
- Updated Postman collection:
    - built-in variables for easier use (See variables specific to the Collection)
    - "Get token" call now extracts and updates {{access_token}} value automatically (no need to copy/paste)
- Added Python client by @Olen (https://github.com/Olen). Thanks and Kudos! The client is a step for Home-assistant.io integration and this is why it is a bit overcomplicated.  

## Integrations
- [home-assistant](https://www.home-assistant.io/) integration. [Plant Monitor component](https://github.com/Olen/homeassistant-plant) and [PlantCard](https://github.com/Olen/lovelace-flower-card) which leverage the component. Discussion of HASS forum [here](https://community.home-assistant.io/t/cloud-plant-db-with-api-for-plantcard/).

## Usage
The easiest way to get familiar with API is to try [API examples](https://documenter.getpostman.com/view/12627470/TVsxBRjD) in Postman. You can either install the free Postman API tool or use its Web version online: https://www.postman.com/

### Examples
For up-to-date examples see [API documentation](https://documenter.getpostman.com/view/12627470/TVsxBRjD)

