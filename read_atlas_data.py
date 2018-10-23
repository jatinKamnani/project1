########################################################################
# IMPORTS

# Installed packages:
import pandas as pd

# Standard Library:
import os.path

########################################################################
# CONSTANTS

# File paths:

DATA_DIR = 'datasets'
HEALTH_DATA_COUNTY_FILE = \
    os.path.join(DATA_DIR, 'cumulative_data_2013_county.csv')
HEALTH_DATA_STATE_FILE = \
    os.path.join(DATA_DIR, 'cumulative_data_2013_state.csv')
########################################################################
# FUNCTIONS


def read_data():
    """Function to simply read the atlas data from file."""
    health_county_data = pd.read_csv(HEALTH_DATA_COUNTY_FILE)
    health_state_data = pd.read_csv(HEALTH_DATA_STATE_FILE)
    # print(health_county_data.head(),health_state_data.head())

    # Return.
    return health_county_data, health_state_data


########################################################################
# MAIN


if __name__ == '__main__':
    read_data()