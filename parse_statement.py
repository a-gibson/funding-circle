#!/usr/bin/python3

import argparse
import os.path
import csv
import re


def readStatement(filename):
    with open(filename, newline='') as csvfile:
        reader_obj = csv.reader(csvfile, delimiter=',', quotechar='"')
        statement = list(reader_obj)

    return statement


def findTransfers(statement):
    transfers = {'in' : 0.0, 'out' : 0.0}

    transfer_in_search_term = 'TRANSFERIN'
    transfer_out_search_term = 'TRANSFEROUT'

    for line in statement:
        in_result = re.search(transfer_in_search_term, line[1])
        if in_result:
            transfers['in'] += float(line[2])

        out_result = re.search(transfer_out_search_term, line[1])
        if out_result:
            transfers['out'] += float(line[3])

    return transfers


def findLoans(statement):
    loans = 0.0

    loan_search_term = 'Loan offer'

    # Go through each line in the statement and search for loans purchased
    for line in statement:
        result = re.match(loan_search_term, line[1])
        if result:
            loans += float(line[3])

    return loans


def findLoanParts(statement):
    loan_parts = {'interest' : 0.0, 'principal' : 0.0, 'transfer_payment' : 0.0}

    loan_part_search_term = 'Loan Part ID (?P<id>\d+)'
    loan_part_ids = set([]) # the set ensures duplicate IDs are not stored
    loan_part_descriptions = []

    interest_search_term = 'Interest [£]*(?P<value>\d+\.\d+)'
    principal_search_term = 'Principal [£]*(?P<value>\d+\.\d+)'
    transfer_payment_search_term = 'Transfer Payment [£]*-(?P<value>\d+\.\d+)'

    # Go through each line of the statement and look for loan parts purchased
    for line in statement:
        result = re.match(loan_part_search_term, line[1])
        if result:
            loan_part_descriptions.append(line[1])
            loan_part_ids.add(result.group('id'))

    # Using the unique list of IDs, find the interest and principal paid to the seller of the loan part and the transfer payment paid to the purchaser
    for loan_id in loan_part_ids:
        for description in loan_part_descriptions:
            description_result = re.search(loan_id, description)
            if description_result:
                interest_result = re.search(interest_search_term, description)
                loan_parts['interest'] += float(interest_result.group('value'))
                principal_result = re.search(principal_search_term, description)
                loan_parts['principal'] += float(principal_result.group('value'))
                transfer_payment_result = re.search(transfer_payment_search_term, description)
                loan_parts['transfer_payment'] += float(transfer_payment_result.group('value'))
                break

    return loan_parts


def calculateFees(statement):
    fees = 0.0
    fee_search_term = 'Servicing fee'

    # Go through each line in the statement and search for servicing fees
    for line in statement:
        result = re.match(fee_search_term, line[1])
        if result:
            fees += float(line[3])

    return fees


def findRepayments(statement):
    repayments = {'interest' : 0.0, 'principal' : 0.0, 'recovery' : 0.0}

    interest_search_term = '(?:Early i|I)nterest repayment'
    principal_search_term = '(?:Early p|P)rincipal repayment'
    recovery_search_term = 'Principal recovery repayment'

    # Go through each line in the statement and search for repayments (interest, principal and recovery)
    for line in statement:
        i_result = re.match(interest_search_term, line[1])
        if i_result:
            repayments['interest'] += float(line[2])

        p_result = re.match(principal_search_term, line[1])
        if p_result:
            repayments['principal'] += float(line[2])

        r_result = re.match(recovery_search_term, line[1])
        if r_result:
            repayments['recovery'] += float(line[2])

    return repayments


def printSummary(transfers, loans, repayments, loan_parts, fee):
    profit_before_fees = repayments['interest'] - loan_parts['interest']
    total_loans_purchased = loans + loan_parts['principal']

    print('')
    print('Outgoings:')
    print('  Total loans/loan parts purchased: £{:.2f}'.format(round(total_loans_purchased, 2)))
    print('  Interest paid due to loan part purchases: £{:.2f}'.format(round(loan_parts['interest'], 2)))
    print('')
    print('Incomings:')
    print('  Principal repaid: £{:.2f}'.format(round(repayments['principal'], 2)))
    print('  Interest received: £{:.2f}'.format(round(repayments['interest'], 2)))
    print('  Bad debt recovery: £{:.2f}'.format(round(repayments['recovery'], 2)))
    print('  Transfer Payment: £{:.2f}'.format(round(loan_parts['transfer_payment'], 2)))
    print('')
    print('Totals:')
    print('  Monies transferred in to Funding Circle:\t£{:.2f}'.format(round(transfers['in'], 2)))
    print('  Monies transferred out of Funding Circle:\t£{:.2f}'.format(round(transfers['out'], 2)))
    print('\t\t\t\t\t\t--------')
    print('  Balance:\t\t\t\t\t£{:.2f}'.format(round(transfers['in'] - transfers['out'], 2)))
    print('')
    print('  Interest received:\t£{:.2f}'.format(round(profit_before_fees, 2)))
    print('  Fees paid:\t\t£{:.2f}'.format(round(fee, 2)))
    print('  Bad debt recovery:\t£{:.2f}'.format(round(repayments['recovery'], 2)))
    print('  Transfer Payment:\t£{:.2f}'.format(round(loan_parts['transfer_payment'], 2)))
    print('\t\t\t--------')
    print('  Balance:\t\t£{:.2f}'.format(round(profit_before_fees - fee + repayments['recovery'] + loan_parts['transfer_payment'], 2)))
    print('')


def parseAndPrint(filename):
    statement = readStatement(filename)

    transfers = findTransfers(statement)

    loans = findLoans(statement)

    loan_parts = findLoanParts(statement)

    fee = calculateFees(statement)

    repayments = findRepayments(statement)

    printSummary(transfers, loans, repayments, loan_parts, fee)


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

    parseAndPrint(args.file)

if __name__ == "__main__":
    main()
