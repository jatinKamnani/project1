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
import plotly.offline
import plotly.plotly as py
import plotly.figure_factory as ff

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

    # How many NaN's do we have?
    total_rows = joined_data.shape[0]
    nan_rows = joined_data.isnull().sum().max()
    joined_data.dropna(inplace=True)
    print('In the joined data, {} rows were be dropped out of {}.'.format(
        nan_rows, total_rows))

    map_plots(joined_data)
    pass


def map_plots(data):
    """Do map plotting.

    plotly reference: https://plot.ly/python/county-choropleth/
    """
    # Plot percentage of lowest income people.
    agi1_bool = data['agi_stub'] == 1
    # Max pct for this on is 61.22
    agi1_pct = (data['total_people_pct_of_FIPS'][agi1_bool] * 100).tolist()
    agi1_fips = data['FIPS'][agi1_bool].tolist()
    pct_bins = list(np.arange(10, 70, 10))
    # colors from http://colorbrewer2.org
    colorscale = ['#f0f9e8', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3',
                  '#2b8cbe', '#08589e']
    fig = ff.create_choropleth(fips=agi1_fips, values=agi1_pct,
                               round_legend_values=True,
                               binning_endpoints=pct_bins,
                               colorscale=colorscale)
    plotly.offline.plot(fig, filename='pct_agi1.html')

    # Plot diabetes. We can still use agi1_bool - the diabetes rate is
    # the same for all agi_stubs.
    diabetes_pct = data['PCT_DIABETES_ADULTS13'][agi1_bool].tolist()
    # We'll re-use the agi1_fips.
    # New pct_bins (max for diabetes is 23.5:
    pct_bins = list(np.arange(5, 26, 5))
    colorscale = ['#f0f9e8', '#ccebc5', '#a8ddb5', '#7bccc4', '#43a2ca',
                  '#0868ac']
    fig = ff.create_choropleth(fips=agi1_fips, values=diabetes_pct,
                               round_legend_values=True,
                               binning_endpoints=pct_bins,
                               colorscale=colorscale)
    plotly.offline.plot(fig, filename='pct_diabetes.html')

    # Plot obesity.
    obesity_pct = data['PCT_OBESE_ADULTS13'][agi1_bool].tolist()
    # We'll re-use the agi1_fips.
    # New pct_bins (max for obesity is 47.6:
    pct_bins = list(np.arange(8, 50, 8))
    colorscale = ['#f0f9e8', '#ccebc5', '#a8ddb5', '#7bccc4', '#4eb3d3',
                  '#2b8cbe', '#08589e']
    fig = ff.create_choropleth(fips=agi1_fips, values=obesity_pct,
                               round_legend_values=True,
                               binning_endpoints=pct_bins,
                               colorscale=colorscale)
    plotly.offline.plot(fig, filename='pct_obese.html')


########################################################################
# MAIN


if __name__ == '__main__':
    data = main()
