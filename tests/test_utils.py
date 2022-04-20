from utils import *


def test_getting_new_forecasts():
    settings = {
        'latitude': 25.877369,
        'longitude': -80.343601,
        'threshold_value': 80,
        'check_in_frequency': 60,
    }
    forecasts = get_updated_forecasts_for_the_next_three_hours(settings)
    assert len(forecasts) == 3


def test_load_settings_txt_file():
    settings = load_settings_from_settings_txt_file()
    assert settings['latitude'] == 25.877369
    assert settings['longitude'] == -80.343601
    assert settings['threshold_value'] == 80
    assert settings['check_in_frequency'] == 60
