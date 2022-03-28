import os
import requests
import xml.etree.ElementTree as ET

dir_path = os.path.dirname(os.path.dirname(__file__))


def extract_variables():
    with open(os.path.join(dir_path, 'settings.txt')) as file:
        lines = file.readlines()
        lines = [line.split('=') for line in lines if '=' in line]
        var_dict = {i[0].strip(): i[1].replace('\n', '').strip() for i in lines}
        return var_dict

def set_variables(dic):
    content = []
    for key, value in dic.items():
        content.append('{} = {}\n'.format(key, value))
    with open(os.path.join(dir_path, 'settings.txt'), "w") as file:
        file.writelines(content)

def get_data_from_noaa(long, lat):
    # fetching the data from NOAA API
    resp = requests.get(r'https://api.weather.gov/points/{},{}'.format(long, lat))
    # selecting the URL for the forcast hourly
    forcast_hourly_url = resp.json()['properties']['forecastHourly']
    print(forcast_hourly_url)

    headers = {
        "accept": "application/vnd.noaa.dwml+xml",
        'Feature - Flag': 'forecast_temperature_qv'
    }
    resp = requests.get(forcast_hourly_url, headers=headers)
    print(resp.status_code)
    root = ET.fromstring(resp.content)
    xpath = r"./data[@type='forecast']/parameters/temperature[2]/value"
    temperature = root.findall(xpath)
    data = [temperature[i].text for i in range(0, 3)]
    forcast_data = {'first_forecast': data[0], 'second_forecast': data[1],
                    'third_forecast': data[2]}
    return forcast_data


def send_alert(hour, temp):
    data = {
        "presetId": 2206,
        "presetName": "Dev Candidate - Evacuate",
        "text": "An EVACUATION ORDER has been issued. In {} hours temperature is expected to be {}F".format(hour, temp)
    }
    url = r'https://demo.alertus.com/alertusmw/services/rest/activation/preset'
    resp = requests.post(url, auth=('devcandidate', 'gooWmJQe'), json=data)
    if resp.status_code == 200:
        return resp.content
    else:
        return 'Error in generating the alert'
