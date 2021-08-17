# Weather Alert
Weather Alert to Alertus System

## Description
This project is an assessment test for dev candidates. The scope of the project is to get the current weather from NOAA (https://api.weather.gov/) (you need to choose and use a US location to be able to retrieve data from NOAA even if you leave outside of US) and use that data on Alertus REST API to activate an alert with the weather information in Alertus Mass Notification System.

## Application Scope
### Runtime of the application
1. Application will read the settings.txt file to get the necessary variables (longitude, latitude, check_in_frequency (in seconds), threshold_value (Degrees in Fahrenheit).
2. Application will start checking the hourly forecast with the time intervals defined in the settings.txt file from NOAA API (https://api.weather.gov) and write the upcoming three hours' forecasted temperatures on a SQLite database table. Database fields: (timestamp, long, lat, first_forecast, second_forecast, third_forecast, alert_generated(Bool, False by default), alert_id(if an alert is activated)
3. If one of the upcoming three hour long period forecasted temperature is higher than the threshold given in the settings file, 
    * activate a preset Alert with custom Alert Message using Alertus API https://demo.alertus.com/alertusmw/services/rest/activation/preset
    * update the SQLite database column "alert_generated" to `True` and alert_id in the respective row.

### Application will have a basic web user interface with 2 sections:
1. **Settings:** It will show the existing settings from the settings.txt file and will give the end user ability to update them. If the settings are updated it will reload the application automatically
2. **Data:** It will show the results of the latest 10 forecast checkins from the SQLite database in a structured html table. It will highlight the row if the row generated an alert. Data will be updated on the page regularly with the intervals of `check_in_frequency`.

### Deliverables
1. application code
2. SQLite Database
3. pipenv environment
4. `RUNTIME_INSTRUCTIONS.md` file for
    - __Instructions to run your code__
    - explanations and highlights (where you are proud of yourself) of your output
    - the list of libraries that you used and why you used them.
    - explaining the challenges that you faced during the task.
5. Your github homepage link

### Rules to follow
1. All deliverables and code has to be submitted as a pull request to this repo
2. Python has to be used as the programming language on the backend. JS can be used for frontend if it is necessary for your application's UI design and interaction.
3. Flask needs to be used as the application framework
4. Bootstrap4 needs to be used for the user interface (the design doesn't have to be beautiful but it needs to show that you are able to use the bootstrap library
5. SQLite needs to be used for database
6. When accessing NOAA API, CAP/XML format needs to be used to retrieve the data using `Accept: application/cap+xml` instead of JSON
7. Alertus API can be used with JSON
8. Internet resources and guides can be used but copy and paste is strictly forbidden. Candidate must be able to explain the code and answer the related questions line by line during the following interview.

### Resources that you can use
1. Alertus REST API Documentation (Swagger) Page: https://demo.alertustech.com/alertusmw/swag.jsp (Credentials will be shared by our HR Representative)
    * Your account have 4 presets ready to use. You can find the preset alerts' ids and details by analyzing the swagger page. You can select any one of them to use
    * You can activate the system using /activation/preset endpoint. The response will return the alert id if the activation was successful. It is expected that you find your way in the documentation without additional assistance.
    * Alertus REST API uses Basic Authentication (with the same credentials that will be shared with you.
    * demo.alertus.com and demo.alertustech.com are different aliases for the same server.
2. NOAA API documentation can be found at: https://www.weather.gov/documentation/services-web-api
3. Our HR Representative will share a windows application link with you with a config file. After downloading the config file and the setup file to the __same directory__ in your windows computer, You can install the application to your computer to receive alerts that you will activate to have a feeling of how Alertus Alerts works. Installation of the application is not necessary for you to complete this task but it will give you an overall acquitance to the Alertus Solution.
4. The task will prove that you are able to code in python and self sufficient by reading online documentation. If you have a major design question which blocks you of completing the task, please send your question to our HR representative.

Good Luck!
