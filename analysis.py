"""
Module for performing analysis/plotting for the report.
"""

########################################################################
# IMPORTS

# Standard library:
import json

# Installed packages:
import pandas as pd
import numpy as np

# Project imports:
import read_atlas_data
import read_irs

########################################################################
# FUNCTIONS


def main():
    """Main function"""
    # Read the IRS data
    irs_data = read_irs.get_irs_data()

    # Notify.
    print('IRS data loaded. Column descriptions:')
    print(json.dumps(read_irs.COLUMNS, indent=2))

    # Read Food Environment Atlas data
    food_county, food_state = read_atlas_data.read_data()
    print('Food Environment Atlas data loaded.')

    # Check to see if the county data has duplicate FIPS codes. Turns
    # out it doesn't.
    # county_duplicate_fips = food_county.duplicated()
    # print(county_duplicate_fips.any())

    # Join the IRS data and county Food Environment Atlas data by FIPS
    # code. Since the IRS data has multiple entries per FIPS code, we'll
    # join on the IRS data
    joined_data = irs_data.join(food_county.set_index('FIPS'), on='FIPS')
    pass


def aggregate_irs_by_fips(irs_data):
    """Function to combine IRS data by FIPS code.

    NOTE: The first draft will be done in a relatively crude way. If we
    need something more sophisticated later, we can do it.
    """
    # Get the listing of unique FIPS codes in the IRS data.
    unique_fips = irs_data['FIPS'].unique()

    # Loop over the unique fips codes and aggregate.


########################################################################
# MAIN


if __name__ == '__main__':
    main()
