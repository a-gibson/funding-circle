from funding_circle.parse_statement import statement # pylint: disable=import-error


def test_find_calculate_fees(test_statement_object):
    """
    Check that Funding Circle fees can be identified and amounts extracted
    Note: numerical values are floats and not strings
    """

    test_statement_object.calculateFees()

    assert test_statement_object.fees == 0.04


def test_read_file(test_data, test_statement_object):
    """
    Check that a CSV file can be read and expressed as a list
    """

    assert test_statement_object.statement == test_data


def test_find_loans(test_statement_object):
    """
    Check that new loan purchases can be identified and amounts extracted
    Note: numerical values are floats and not strings
    """

    test_statement_object.findLoans()

    assert test_statement_object.loans == 40.0


def test_find_loan_parts(test_statement_object):
    """
    Check that loan parts (as sold by other investors) can be identified and amounts extracted
    Note: numerical values are floats and not strings
    """

    test_statement_object.findLoanParts()

    assert test_statement_object.loan_parts['interest'] == 0.37
    assert test_statement_object.loan_parts['principal'] == 46.09
    assert test_statement_object.loan_parts['transfer_payment'] == 0.1


def test_find_repayments(test_statement_object):
    """
    Check that loan repayments (from debtors) can be identified and amounts extracted
    Note: numerical values are floats and not strings
    """

    test_statement_object.findRepayments()

    assert test_statement_object.repayments['interest'] == 0.04
    assert test_statement_object.repayments['principal'] == 1.28
    assert test_statement_object.repayments['recovery'] == 0.07

def test_find_transfers(test_statement_object):
    """
    Check that balance transfers can be identified and amounts extracted
    Note: numerical values are floats and not strings
    """

    test_statement_object.findTransfers()

    assert test_statement_object.transfers['in'] == 10000.0
    assert test_statement_object.transfers['out'] == 5000.0
