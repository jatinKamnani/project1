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
from fipsZipHandler import FipsZipHandler

########################################################################
# FUNCTIONS


def main():
    """Main function"""
    # Read the IRS data
    irs_data = read_irs.read_data()

    # Convert zipcode to a string. Note: it'd be more efficient to
    # define the data type when the file is read, but that can be a real
    # hassle.
    irs_data['zipcode'] = irs_data['zipcode'].astype(str)

    # Notify.
    print('IRS data loaded. Column descriptions:')
    print(json.dumps(read_irs.COLUMNS, indent=2))

    # Read Food Environment Atlas data
    food_county, food_state = read_atlas_data.read_data()
    print('Food Environment Atlas data loaded.')

    # Initialize FipsZipHandler object
    fz_obj = FipsZipHandler()

    # Translate IRS data zip codes to FIPS codes.
    irs_fips = [fz_obj.getFipsForZipcode(z) for z in irs_data['zipcode']]

    # Add column to irs_data for fips code.
    irs_data['FIPS'] = irs_fips

    # Remove leading 0's from IRS FIPS codes (Food Environment Atlas
    # doesn't have them, and it's easier/more robust to just drop the
    # leading 0's.
    irs_data['FIPS'] = irs_data['FIPS'].str.replace(pat='^0', repl='',
                                                    regex=True)
    # Sanity check (should evaluate to False, and it does):
    # irs_data['FIPS'].str.startswith('0').any()

    # Check to see if the county data has duplicate FIPS codes. Turns
    # out it doesn't.
    # county_duplicate_fips = food_county.duplicated()
    # print(county_duplicate_fips.any())

    # Join the IRS data and county Food Environment Atlas data by FIPS
    # code. Since the IRS data has multiple entries per FIPS code, we'll
    # join on the IRS data
    joined_data = irs_data.join(food_county.set_index('FIPS'), on='FIPS')
    pass

########################################################################
# MAIN


if __name__ == '__main__':
    main()
