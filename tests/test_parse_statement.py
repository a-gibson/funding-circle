from funding_circle.parse_statement import statement


def test_read_csv_file(test_data, test_statement_location):
    """
    Check that a CSV file can be read and expressed as a list
    """

    s = statement(test_statement_location)
    s.readFile()

    assert s.statement == test_data
