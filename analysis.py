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

    # Compute the wealth per person for the irs data.
    irs_data_agg = wealth_per_person(irs_data_agg)
    irs_data_no_agg = wealth_per_person(irs_data_no_agg)

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


def wealth_per_person(irs_data):
    """Estimate wealth per person with the IRS data.

    Note
    """
    # Single returns + 2 * joint returns + number of dependents.
    # NOTE: It seems that head of household (MARS4) is not mutually
    # exclusive with MARS1. So we'll exclude it.
    irs_data['total_people'] = (irs_data['MARS1'] + 2 * irs_data['MARS2']
                                + irs_data['NUMDEP'])

    # Divide AGI by the number of people.
    # NOTE: It would seem that the IRS AGI number needs to be multiplied
    # by 1000. This is evidenced by taking irs_data['A00100']
    # / irs_data['N1'] and noticing that all the values correctly fall
    # in the irs_data['agi_stub'] categories.
    irs_data['agi_per_person'] = irs_data['A00100'] / irs_data['total_people']

    return irs_data

########################################################################
# MAIN


if __name__ == '__main__':
    main()
