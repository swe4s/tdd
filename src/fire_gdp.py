
"""
Read and combine forest fire emissions and GDP data from CSV files.

Functions are provided to read CSV data, locate columns by name,
and match annual forest fire emissions with GDP for a country.
"""

import csv


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    """
    Read rows from a CSV file with optional filtering.

    Parameters
    ----------
    file_name : str
        Path to the CSV file.
    query_column : int or None
        Column index used to filter rows.
    query_value : str or None
        Value to match in the query column.
    return_header : bool
        Whether to return the header along with the data rows.

    Returns
    -------
    list or tuple
        List of matching rows, or a tuple containing the header
        and matching rows when return_header is True.
    """
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)

        # Read the header separately from the data rows.
        header = next(reader)

        rows = []

        for row in reader:
            # Include all rows when no filter is provided.
            if query_column is None or query_value is None:
                rows.append(row)

            # Otherwise, include only rows matching the query.
            elif row[query_column] == query_value:
                rows.append(row)

    if return_header:
        return header, rows

    return rows


def get_column_index(header, column_name):
    """
    Find the index of a specified column in a header list.

    Parameters
    ----------
    header : list
        List containing column names.
    column_name : str
        Name of the column to locate.

    Returns
    -------
    int or None
        Index of the column, or None if the name is not found.
    """
    try:
        return header.index(column_name)

    except ValueError:
        # Return None when the requested column does not exist.
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    """
    Combine annual forest fire emissions and GDP for a country.

    Parameters
    ----------
    co2_file : str
        Path to the forest fire emissions CSV file.
    gdp_file : str
        Path to the GDP CSV file.
    country : str
        Country to retrieve and match across both datasets.

    Returns
    -------
    list
        List of [year, forest_fires, gdp] entries.
        Years are integers, and emissions and GDP are floats.
        Years with missing values are excluded.
    """
    # Retrieve the CO2 header and rows for the selected country.
    co2_header, co2_rows = get_data(
        co2_file,
        query_column=0,
        query_value=country,
        return_header=True
    )

    # Retrieve the GDP header and rows for the same country.
    gdp_header, gdp_rows = get_data(
        gdp_file,
        query_column=0,
        query_value=country,
        return_header=True
    )

    # Identify the forest fire emissions column.
    fire_index = get_column_index(co2_header, 'Forest fires')

    results = []

    # Each CO2 row represents a specific country and year.
    for row in co2_rows:
        year = row[1]
        forest_fires = row[fire_index]

        # Skip years with missing forest fire emissions.
        if forest_fires == '':
            continue

        forest_fires = float(forest_fires)

        # Find the corresponding year in the GDP header.
        gdp_year_idx = get_column_index(gdp_header, year)

        # Skip years that are not present in the GDP dataset.
        if gdp_year_idx is None:
            continue

        # Get GDP from the country's matching row and year.
        gdp_value = gdp_rows[0][gdp_year_idx]

        # Skip years with missing GDP data.
        if gdp_value == '':
            continue

        # Convert values to the required numerical types.
        year = int(year)
        gdp_value = float(gdp_value)

        # Store the matched year, emissions, and GDP values.
        results.append([year, forest_fires, gdp_value])

    return results
