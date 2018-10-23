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
           'A00100': 'Adjusted gross income (AGI)'}

########################################################################
# FUNCTIONS


def read_data():
    """Function to simply read the IRS data from file."""
    irs_data = pd.read_csv(IRS_FILE_PATH, header=0,
                           usecols=list(COLUMNS.keys()))
    pass


########################################################################
# MAIN


if __name__ == '__main__':
    read_data()
