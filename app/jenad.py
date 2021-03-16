# Infinite loop for updating a file for machine learning purposes
# This code was originally copied from synopsisd
# FIXME : is the wind speed adjusted for 2m pole ?

import time
import traceback
from pprint import pprint

# artifacts (metfuncs)
# import wet_bulb
# import synopsis
# import okta_funcs
# import solar_rad_expected
import wind_calibration

# artifacts (metrestapi)
import cumulus_comms

# imports
import get_cumulus_weather_info
import get_env
import get_env_app
import definitions
import append_mlearning_rec
import sync_start_time

# Add a bunch of reliability code to this before deploying

def main():
    try:
        weather_info = {}
        my_app_name = 'jenad'
        version = get_env.get_version()
        verbose = get_env.get_verbose()
        stage = get_env.get_stage()

        cumulusmx_endpoint = get_env.get_cumulusmx_endpoint()
        mins_between_updates = get_env_app.get_mins_between_updates()
        vane_height_m = get_env_app.get_vane_height_m()

        wind_speed_multiplier = wind_calibration.calc_vane_height_to_10m_multiplier(vane_height_m)

        lat = 51.4151   # Stockcross
        lon = -1.3776   # Stockcross

        print(my_app_name + ' started, version=' + version)
        print('stage=' + stage)
        if stage == 'DEV':
            verbose = True
        print('verbose=' + verbose.__str__())
        print('cumulusmx endpoint=' + cumulusmx_endpoint)

        print('waiting to sync main loop...')
        sync_start_time.wait_until_minute_flip(10)

        print('entering main loop...')
        while True:
            start_secs = time.time()
            cumulus_weather_info = get_cumulus_weather_info.get_key_weather_variables(cumulusmx_endpoint)     # REST API call
            # cumulus_weather_info = None
            if cumulus_weather_info is None:        # can't talk to CumulusMX
                print('Error: CumulusMX did not return valid data')
                cumulus_comms.wait_until_cumulus_data_ok(cumulusmx_endpoint)  # loop until CumulusMX data is OK
                continue

            weather_info['pressure'] = float(cumulus_weather_info['Pressure'])
            weather_info['temp'] = float(cumulus_weather_info['OutdoorTemp'])
            weather_info['dew_point'] = float(cumulus_weather_info['OutdoorDewpoint'])
            weather_info['feels_like'] = float(cumulus_weather_info['FeelsLike'])
            weather_info['humidity'] = float(cumulus_weather_info['OutdoorHum'])
            weather_info['wind_speed'] = round(float(cumulus_weather_info['WindAverage']) * wind_speed_multiplier, 1)  # FIXME my vane is approx 4m above ground not 2m
            weather_info['wind_gust'] = float(cumulus_weather_info['Recentmaxgust'])
            weather_info['wind_deg'] = int(cumulus_weather_info['Bearing'])

            append_mlearning_rec.append_mlearning_info(weather_info)

            stop_secs = time.time()
            sleep_secs = (mins_between_updates * 60) - (stop_secs - start_secs)
            time.sleep(sleep_secs)

    except Exception as e:
        print('Error : ' + e.__str__())
        traceback.print_exc()


if __name__ == '__main__':
    main()

