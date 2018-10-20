########################################################################
# IMPORTS

# Installed packages:
import pandas as pd

# Standard Library:
import os.path

########################################################################
# CONSTANTS

# File paths:


HEALTH_DATA_COUNTY_FILE = 'C:/Users/jatin/Desktop/project1/project1/datasets/cumulative_data_2013_county.csv'
HEALTH_DATA_STATE_FILE = 'C:/Users/jatin/Desktop/project1/project1/datasets/cumulative_data_2013_state.csv'
########################################################################
# FUNCTIONS


def read_data():
    """Function to simply read the IRS data from file."""
    health_county_data = pd.read_csv(HEALTH_DATA_COUNTY_FILE)
    health_state_data = pd.read_csv(HEALTH_DATA_STATE_FILE)
    print(health_county_data.head(),health_state_data.head())
    pass


########################################################################
# MAIN


if __name__ == '__main__':
    read_data()