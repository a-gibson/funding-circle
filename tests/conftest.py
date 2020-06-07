import pytest

from funding_circle.parse_statement import statement


@pytest.fixture(scope='session')
def test_statement_location():
    yield 'tests/test_statement.csv'


@pytest.fixture(scope='session')
def test_data():
    data = [
        ['Date', 'Description', 'Paid In', 'Paid Out'],
        ['2000-01-01', 'Principal repayment for loan part 12345678', '0.38', ''],
        ['2000-01-01', 'Interest repayment for loan part 12345678', '0.03', '']
    ]

    yield data
