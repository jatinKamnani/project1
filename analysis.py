"""
Module for performing analysis/plotting for the report.
"""

########################################################################
# IMPORTS

# Standard library:
import json

# Installed packages:
import pandas as pd

# Project imports:
import read_atlas_data
import read_irs

########################################################################
# FUNCTIONS


def main():
    """Main function"""
    # Read the IRS data
    irs_data = read_irs.read_data()
    print('IRS data loaded. Column descriptions:')
    print(json.dumps(read_irs.COLUMNS, indent=2))

    # Read Food Environment Atlas data
    food_county, food_state = read_atlas_data.read_data()

    pass

########################################################################
# MAIN


if __name__ == '__main__':
    main()
