"""
Module for reading IRS data. To be consistent with health data, we're
using 2013 data.

As described in the README.md file, this module expects you to have a
folder called 'zipcode2013' in this directory. Within this directory,
at the minimum a file called '13zpallagi.csv'

NOTE: The IRS data excludes those with a gross deficit
(rather than income).
"""
########################################################################
# IMPORTS

# Installed packages:
import pandas as pd

# Standard Library:
import os.path

# Project modules:
from fipsZipHandler import FipsZipHandler

########################################################################
# CONSTANTS

# File paths:
# Folder w/ IRS data in it.
IRS_DIR = 'zipcode2013'
# IRS data file name.
IRS_FILE = 'zipcodeagi13.csv'
# Full path to IRS data file.
IRS_FILE_PATH = os.path.join('.', IRS_DIR, IRS_FILE)

# Columns to read. Keys are columns, values are brief explanations.
COLUMNS = {'STATEFIPS': 'State FIPS code',
           'STATE': 'Two letter state code', 'zipcode': 'Zip code',
           'agi_stub': ('Code for income bracket. 1: $1-$25k, 2: $25k-$50k, '
                        + '3: $50k-$75k, 4: $75k-$100k, 5: $100k-$200k, '
                        + '6: $200k+'),
           'N1': '# of returns',
           'MARS1': '# of single returns',
           'MARS2': '# of joint returns',
           'MARS4': '# of head of household returns',
           'NUMDEP': '# of dependents',
           'A00100': 'Adjusted gross income (AGI)',
           'A02650': 'Total income amount'}

########################################################################
# FUNCTIONS


def read_data():
    """Function to simply read the IRS data from file."""
    irs_data = pd.read_csv(IRS_FILE_PATH, header=0,
                           usecols=list(COLUMNS.keys()))

    # Convert zipcode to a string. Note: it'd be more efficient to
    # define the data type when the file is read, but that can be a real
    # hassle.
    irs_data['zipcode'] = irs_data['zipcode'].astype(str)

    # Convert STATEFIPS to a string. Same efficiency note as above.
    irs_data['STATEFIPS'] = irs_data['STATEFIPS'].astype(str)

    return irs_data


def lookup_fips(irs_data):
    """Function to associate FIPS codes based on IRS zipcodes"""
    # Initialize FipsZipHandler object
    fz_obj = FipsZipHandler()

    # Translate IRS data zip codes to FIPS codes.
    irs_fips = [fz_obj.getFipsForZipcode(z) for z in irs_data['zipcode']]

    # Add column to irs_data for FIPS code.
    irs_data['FIPS'] = irs_fips

    # Return.
    return irs_data


def aggregate_by_fips(irs_data):
    """Function to combine IRS data by FIPS code.

    NOTE: This doesn't necessarily need to be in a function since pandas
    makes this so easy.
    """
    # Drop NaN state values.
    irs_data.dropna(inplace=True)

    # Use groupby to aggregate.
    aggregated_data = irs_data.groupby(['FIPS', 'agi_stub']).sum()

    # For simplicity, change the multi-index into columns.
    # TODO: We may want to keep the multi-index around?
    aggregated_data.reset_index(inplace=True)

    return aggregated_data


def get_irs_data():
    """Main function to load, map, and aggregate IRS data.
    """
    # Read file.
    data_no_aggregation = read_data()

    # Get FIPS for all zip codes.
    data_no_aggregation = lookup_fips(data_no_aggregation)

    # Aggregate by FIPS codes.
    data_aggregated = aggregate_by_fips(data_no_aggregation)

    return data_aggregated, data_no_aggregation

########################################################################
# MAIN


if __name__ == '__main__':
    get_irs_data()
