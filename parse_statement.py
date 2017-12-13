#!/usr/local/bin/python3

import argparse
import os.path
import csv
import re


def findTransfers(file):
    transfer_in = 0.0
    transfer_out = 0.0
    transfer_in_search_term = 'TRANSFERIN'
    transfer_out_search_term = 'TRANSFEROUT'

    with open(file, newline='') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='"')

        for line in statement:
            in_result = re.search(transfer_in_search_term, line[1])
            if in_result:
                transfer_in += float(line[2])

            out_result = re.search(transfer_out_search_term, line[1])
            if out_result:
                transfer_out += float(line[3])

    return transfer_in, transfer_out


def findLoans(file):
    loan = 0.0
    loan_search_term = 'Loan offer'

    with open(file, newline='') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Go through each line in the statement and search for loans purchased
        for line in statement:
            result = re.match(loan_search_term, line[1])
            if result:
                loan += float(line[3])

    return loan


def findLoanParts(file):
    interest = 0.0
    principal = 0.0
    loan_part_search_term = 'Loan Part ID (?P<id>\d+)'
    loan_part_ids = set([]) # the set ensures duplicate IDs are not stored
    loan_part_descriptions = []

    interest_search_term = 'Interest (?P<value>\d+.\d+)'
    principal_search_term = 'Principal (?P<value>\d+.\d+)'

    with open(file, newline='') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Go through each line of the statement and look for loan parts purchased
        for line in statement:
            result = re.match(loan_part_search_term, line[1])
            if result:
                loan_part_descriptions.append(line[1])
                loan_part_ids.add(result.group('id'))

    # Using the unique list of IDs, find the interest and principal paid to the seller of the loan part
    for loan_id in loan_part_ids:
        for description in loan_part_descriptions:
            description_result = re.search(loan_id, description)
            if description_result:
                interest_result = re.search(interest_search_term, description)
                interest += float(interest_result.group('value'))
                principal_result = re.search(principal_search_term, description)
                principal += float(principal_result.group('value'))
                break

    return interest, principal


def calculateFees(file):
    fees = 0.0
    fee_search_term = 'Servicing fee'

    with open(file, newline='') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Go through each line in the statement and search for servicing fees
        for line in statement:
            result = re.match(fee_search_term, line[1])
            if result:
                fees += float(line[3])

    return fees


def findRepayments(file):
    interest = 0.0
    principal = 0.0
    interest_search_term = '(?:Early i|I)nterest repayment'
    principal_search_term = '(?:Early p|P)rincipal repayment'

    with open(file, newline='') as csvfile:
        statement = csv.reader(csvfile, delimiter=',', quotechar='"')

        # Go through each line in the statement and search for repayments (interest and principal)
        for line in statement:
            i_result = re.match(interest_search_term, line[1])
            if i_result:
                interest += float(line[2])

            p_result = re.match(principal_search_term, line[1])
            if p_result:
                principal += float(line[2])

    return interest, principal


def printSummary(transfer_in, transfer_out, loan, repayment_interest, repayment_principal, loan_part_interest, loan_part_principal, fee):
    profit_before_fees = repayment_interest - loan_part_interest
    total_loans_purchased = loan + loan_part_principal

    print('')
    print('Outgoings:')
    print('Total loans/loan parts purchased: £{}'.format(round(total_loans_purchased, 2)))
    print('Interest paid due to loan part purchases: £{}'.format(round(loan_part_interest, 2)))
    print('')
    print('Incomings:')
    print('Principal repaid: £{}'.format(round(repayment_principal, 2)))
    print('Interest received: £{}'.format(round(repayment_interest, 2)))
    print('')
    print('----- ----- ----- ----- -----')
    print('')
    print('Total monies transferred in to Funding Circle: £{}'.format(round(transfer_in, 2)))
    print('Total monies transferred out of Funding Circle: £{}'.format(round(transfer_out, 2)))
    print('Total interest: £{}'.format(round(profit_before_fees, 2)))
    print('Total fees: £{}'.format(round(fee, 2)))
    print('')


def main():
    parser = argparse.ArgumentParser(description='Calculate total income from Funding Circle monthly statement.')

    parser.add_argument(
        '--file',
        default='.',
        help='Path to the monthly statement.')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print('File "{}" does not exist.'.format(args.file))
        exit(1)

    transfer_in, transfer_out = findTransfers(args.file)

    loan = findLoans(args.file)

    loan_part_interest, loan_part_principal = findLoanParts(args.file)

    fee = calculateFees(args.file)

    repayment_interest, repayment_principal = findRepayments(args.file)

    printSummary(transfer_in, transfer_out, loan, repayment_interest, repayment_principal, loan_part_interest, loan_part_principal, fee)


if __name__ == "__main__":
    main()
