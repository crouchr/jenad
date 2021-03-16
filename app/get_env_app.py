# environment specific to this app
import os


def get_mins_between_updates():
    """
    Set time between consecutive updates
    """

    if 'MINS_BETWEEN_UPDATES' in os.environ:
        mins_between_updates = int(os.environ['MINS_BETWEEN_UPDATES'])
    else:
        mins_between_updates = 10    # was 15

    return mins_between_updates


# Actual wind vane height to allow for multiplier
def get_vane_height_m():
    if 'VANE_HEIGHT' in os.environ:
        vane_height = os.environ['VANE_HEIGHT']
    else:
        vane_height = 3.7       # value in Ermin Street

    return vane_height