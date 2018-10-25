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
    irs_data_agg, irs_data_no_agg = read_irs.get_irs_data()

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
    joined_data = irs_data_agg.join(food_county.set_index('FIPS'), on='FIPS')

    # How many NaN's do we have?
    total_rows = joined_data.shape[0]
    nan_rows = joined_data.isnull().sum().max()
    joined_data.dropna(inplace=True)
    print('In the joined data, {} rows were be dropped out of {}.'.format(
        nan_rows, total_rows))
    pass

########################################################################
# MAIN


if __name__ == '__main__':
    main()
