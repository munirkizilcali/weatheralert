# WeatherAlert - Integrating Alertus Solutions With Weather Data
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Description
WeatherAlert is a simple web application that utilizes the Alertus Solutions and forecast data based on geographical location. The website will display a table holding different forecasts and wether or not they have generated an alert. The alert is stored in a sqlite3 database with a unique ID.

## Installation
##### Note: this project assumes a default python version of 3 or later. It has not been tested on any 2.x distribution.

1. We're using a tool called [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) to manage our work environment. To start it simply type ```workon weatheralert```.

![Virtual environment setup](https://github.com/snaraj/weatheralert/blob/master/assets/images/virtual_env_setup.png?raw=true)

2. After our virtual environment has been set up, we can install our project dependencies. Run ```pip3 install -r requirements.txt``` while on the root of the project.

3. Since we are using Flask, we need to set up a few environment variables so we can operate out of the command line without issues.

![Flask setup](https://github.com/snaraj/weatheralert/blob/master/assets/images/flask_setup.png?raw=true)

## Usage

1. To start our local server, we type ```flask run``` on the root folder. It should look like this.
![Flask run](https://github.com/snaraj/weatheralert/blob/master/assets/images/flask_run.png?raw=true)

2. Once loaded, you will be greeted with two different components; a settings, and a data table component.
![Settings](https://github.com/snaraj/weatheralert/blob/master/assets/images/settings.png?raw=true)

![Data](https://github.com/snaraj/weatheralert/blob/master/assets/images/data.png?raw=true)

3. You can interact with the webpage by providing different (valid) coordinates as well as changing the threshold value. The Threshold Value is important since it determines wether the Alertus Solutions generates an alert or not. The screenshot below shows how it would look like after updating the website with a Threshold Value of 37.

![Data Updated](https://github.com/snaraj/weatheralert/blob/master/assets/images/data_updated.png?raw=true)

## Credits & Miscellanea
    - Alertus: https://www.alertus.com/
    - NOAA: https://www.weather.gov/documentation/services-web-api

    - List of libraries: See requirements.txt

    - Challenges:
        - Being able to update the data table dynamically based on the new settings passed by the user.
        - Updating Jinja2 template dynamically using JavaScript.
        - Moving data through different API's while conserving integrity.
        - Authenticating our API usage. 
    
    - Highlights:
        - Was able to solve all of the problems above.
        - I was able to figure out many things that I had never implemented before.
        - App works as expected, described by the documentation posted.
        - Overall this project was an amazing learning experience.