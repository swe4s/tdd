
"""
Unit tests for forest fire emissions and GDP data processing.

Tests verify CSV reading, column identification, country filtering,
header retrieval, and matching forest fire emissions with GDP data.
"""

import unittest

import fire_gdp


class TestGetColumnIndex(unittest.TestCase):
    """Test identification of column indices in CSV headers."""

    def test_name_present(self):
        """Verify that an existing column returns its index."""
        header = ['Area', 'Year', 'Forest fires']

        result = fire_gdp.get_column_index(header, 'Year')

        self.assertEqual(result, 1)

    def test_name_missing(self):
        """Verify that a missing column returns None."""
        header = ['Area', 'Year', 'Forest fires']

        result = fire_gdp.get_column_index(header, 'GDP')

        self.assertIsNone(result)

    def test_empty_header(self):
        """Verify that an empty header returns None."""
        header = []

        result = fire_gdp.get_column_index(header, 'Year')

        self.assertIsNone(result)


class TestGetData(unittest.TestCase):
    """Test reading and filtering rows from CSV files."""

    def test_get_all_rows(self):
        """Verify that all data rows are returned without a filter."""
        file_name = 'test/data/test_co2.csv'

        result = fire_gdp.get_data(file_name)

        expected = [
            ['Brazil', '2000', '150.5'],
            ['Brazil', '2001', '200.2'],
            ['Brazil', '2002', ''],
            ['Canada', '2000', '75.3']
        ]

        self.assertEqual(result, expected)

    def test_filter_country(self):
        """Verify that only rows matching a country are returned."""
        file_name = 'test/data/test_co2.csv'

        result = fire_gdp.get_data(
            file_name,
            query_column=0,
            query_value='Brazil'
        )

        expected = [
            ['Brazil', '2000', '150.5'],
            ['Brazil', '2001', '200.2'],
            ['Brazil', '2002', '']
        ]

        self.assertEqual(result, expected)

    def test_return_header(self):
        """Verify that the header and all rows are returned."""
        file_name = 'test/data/test_co2.csv'

        result = fire_gdp.get_data(
            file_name,
            return_header=True
        )

        expected_header = ['Area', 'Year', 'Forest fires']

        expected_rows = [
            ['Brazil', '2000', '150.5'],
            ['Brazil', '2001', '200.2'],
            ['Brazil', '2002', ''],
            ['Canada', '2000', '75.3']
        ]

        self.assertEqual(result, (expected_header, expected_rows))

    def test_filter_country_with_header(self):
        """Verify that country filtering also returns the header."""
        file_name = 'test/data/test_co2.csv'

        result = fire_gdp.get_data(
            file_name,
            query_column=0,
            query_value='Brazil',
            return_header=True
        )

        expected_header = ['Area', 'Year', 'Forest fires']

        expected_rows = [
            ['Brazil', '2000', '150.5'],
            ['Brazil', '2001', '200.2'],
            ['Brazil', '2002', '']
        ]

        self.assertEqual(result, (expected_header, expected_rows))


class TestGetFireGdpYearData(unittest.TestCase):
    """Test matching forest fire emissions and GDP by country and year."""

    def test_brazil_2000(self):
        """Verify year matching, numerical conversion, and missing data."""
        co2_file = 'test/data/test_co2.csv'
        gdp_file = 'test/data/test_gdp.csv'
        country = 'Brazil'

        # Retrieve combined fire emissions and GDP for Brazil.
        result = fire_gdp.get_fire_gdp_year_data(
            co2_file,
            gdp_file,
            country
        )

        # The year 2002 is excluded because fire emissions are missing.
        expected = [
            [2000, 150.5, 1000.0],
            [2001, 200.2, 1200.0]
        ]

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
