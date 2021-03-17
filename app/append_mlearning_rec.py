# append a weather record for consumption by Machine Learning
# Format is very similar to jena weather training set as per 'Deep Learning with Python' page 207

import definitions
import traceback






# Should be able to import this file direct into the Weather examples in Deep Learning with Python
def append_mlearning_info(weather_info, record_timestamp):
    """
    Append a simple record to mlearning.csv

    :param weather_info:
    :return:
    """
    try:
        mlearning_log_filename = definitions.JENAD_ROOT + 'mlearning.csv'

        mlearning_rec = record_timestamp + ',' + \
            weather_info['pressure'].__str__() + ',' + \
            weather_info['temp'].__str__() + ',' + \
            weather_info['dew_point'].__str__() + ',' + \
            weather_info['feels_like'].__str__() + ',' + \
            float(weather_info['humidity']).__str__() + ',' + \
            weather_info['wind_speed'].__str__() + ',' + \
            weather_info['wind_gust'].__str__() + ',' + \
            weather_info['wind_deg'].__str__() + '\n'

        print('mlearning_rec appended to ' + mlearning_log_filename + ' => ' + mlearning_rec.rstrip('\n'))

        fp_out = open(mlearning_log_filename, 'a')
        fp_out.write(mlearning_rec)
        fp_out.close()
        return True

    except Exception as e:
        traceback.print_exc()
        return False
