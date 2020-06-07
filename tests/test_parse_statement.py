from funding_circle.parse_statement import statement


def test_read_csv_file():
    """
    Check that a CSV can be read and expressed as a list
    """

    # TODO - Share this data object across multiple tests
    test_data = [
        ['Date', 'Description', 'Paid In', 'Paid Out'],
        ['2000-01-01', 'Principal repayment for loan part 12345678', '0.38', ''],
        ['2000-01-01', 'Interest repayment for loan part 12345678', '0.03', '']
    ]
    test_file = 'tests/test_statement.txt'

    s = statement(test_file)

    s.readFile()
    assert s.statement == test_data
