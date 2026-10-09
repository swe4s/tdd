"""Generate scatter plots of forest fire emissions versus GDP."""

import argparse
import sys

import matplotlib
import matplotlib.pyplot as plt

from fire_gdp import get_fire_gdp_year_data


def main():
    """
    Generate and save a forest fire emissions versus GDP scatter plot.

    Command-line arguments allow the user to specify the country
    and output filename.

    Returns
    -------
    int
        Exit code of 0 for success or 1 if no matching data exists.
    """

    # Use a non-interactive backend to save plots without a display.
    matplotlib.use('Agg')

    # Define command-line arguments for the output file and country.
    parser = argparse.ArgumentParser(
        description='Plot forest fire emissions against GDP.'
    )

    parser.add_argument('--out', default='fire_gdp.png')
    parser.add_argument('--country', default='Brazil')

    args = parser.parse_args()

    # Define the paths to the input datasets.
    co2_file = 'data/Agrofood_co2_emission.csv'
    gdp_file = 'data/IMF_GDP.csv'

    # Retrieve matched forest fire emissions and GDP values.
    data = get_fire_gdp_year_data(
        co2_file,
        gdp_file,
        args.country
    )

    # Stop if no matching data is available for the country.
    if not data:
        print('No matching data for ' + args.country)
        return 1

    # Extract the variables used in the scatter plot.
    fires = [row[1] for row in data]
    gdp = [row[2] for row in data]

    # Create a scatter plot showing the relationship between GDP
    # and forest fire emissions.
    fig, ax = plt.subplots()
    ax.scatter(gdp, fires)

    # Label the axes and identify the selected country.
    ax.set_xlabel('GDP (millions of local currency)')
    ax.set_ylabel('Forest fire emissions')
    ax.set_title(args.country + ': Forest Fires vs GDP')

    # Save the plot and close the figure to release resources.
    fig.tight_layout()
    fig.savefig(args.out)
    plt.close(fig)

    print('Created ' + args.out)

    return 0


if __name__ == '__main__':
    sys.exit(main())
