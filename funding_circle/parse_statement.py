#!/usr/bin/env python3

import argparse
import os.path
import csv
import re


class statement:
    def __init__(self, path):
        self.fees = 0.0
        self.loans = 0.0
        self.loan_parts = {'interest' : 0.0, 'principal' : 0.0, 'transfer_payment' : 0.0}
        self.path = path
        self.repayments = {'interest' : 0.0, 'principal' : 0.0, 'recovery' : 0.0}
        self.statement = []
        self.transfers = {'in' : 0.0, 'out' : 0.0}

    def readFile(self):
        with open(self.path, newline='') as csvfile:
            reader_obj = csv.reader(csvfile, delimiter=',', quotechar='"')
            self.statement = list(reader_obj)

    def findTransfers(self):
        transfer_in_search_term = r'TRANSFERIN'
        transfer_out_search_term = r'TRANSFEROUT'

        for line in self.statement:
            in_result = re.search(transfer_in_search_term, line[1])
            if in_result:
                self.transfers['in'] += float(line[2])

            out_result = re.search(transfer_out_search_term, line[1])
            if out_result:
                self.transfers['out'] += float(line[3])

    def findLoans(self):
        loan_search_term = r'Loan offer'

        # Go through each line in the statement and search for loans purchased
        for line in self.statement:
            result = re.match(loan_search_term, line[1])
            if result:
                self.loans += float(line[3])

    def findLoanParts(self):
        loan_part_search_term = r'Loan Part ID (?P<id>\d+)'
        loan_part_ids = set([]) # the set ensures duplicate IDs are not stored
        loan_part_descriptions = []

        interest_search_term = r'Interest [£]?(?P<value>\d+\.\d+)'
        principal_search_term = r'Principal [£]?(?P<value>\d+\.\d+)'
        transfer_payment_search_term = r'Transfer Payment [£]?-(?P<value>\d+\.\d+)'

        # Go through each line of the statement and look for loan parts purchased
        for line in self.statement:
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
                    if interest_result:
                        self.loan_parts['interest'] += float(interest_result.group('value'))

                    principal_result = re.search(principal_search_term, description)
                    if principal_result:
                        self.loan_parts['principal'] += float(principal_result.group('value'))

                    transfer_payment_result = re.search(transfer_payment_search_term, description)
                    if transfer_payment_result:
                        self.loan_parts['transfer_payment'] += float(transfer_payment_result.group('value'))

                    break

    def calculateFees(self):
        fee_search_term = r'Servicing fee'

        # Go through each line in the statement and search for servicing fees
        for line in self.statement:
            result = re.match(fee_search_term, line[1])
            if result:
                self.fees += float(line[3])

    def findRepayments(self):
        interest_search_term = r'(?:Early i|I)nterest repayment'
        principal_search_term = r'(?:Early p|P)rincipal repayment'
        recovery_search_term = r'(Interest|Principal) recovery repayment'

        # Go through each line in the statement and search for repayments (interest, principal and recovery)
        for line in self.statement:
            i_result = re.match(interest_search_term, line[1])
            if i_result:
                self.repayments['interest'] += float(line[2])

            p_result = re.match(principal_search_term, line[1])
            if p_result:
                self.repayments['principal'] += float(line[2])

            r_result = re.match(recovery_search_term, line[1])
            if r_result:
                self.repayments['recovery'] += float(line[2])

    def printSummary(self):
        profit_before_fees = self.repayments['interest'] - self.loan_parts['interest']
        total_loans_purchased = self.loans + self.loan_parts['principal']

        print('')
        print('Outgoings:')
        print('  Total loans/loan parts purchased:\t\t£{:.2f}'.format(round(total_loans_purchased, 2)))
        print('  Interest paid due to loan part purchases:\t£{:.2f}'.format(round(self.loan_parts['interest'], 2)))
        print('  Fees paid to Funding Circle:\t\t\t£{:.2f}'.format(round(self.fees, 2)))
        print('\t\t\t\t\t\t--------')
        print('  Total outgoings:\t\t\t\t£{:.2f}'.format(round(total_loans_purchased + self.loan_parts['interest'] + self.fees, 2)))
        print('')
        print('Incomings:')
        print('  Principal repaid:\t\t\t\t£{:.2f}'.format(round(self.repayments['principal'], 2)))
        print('  Interest received:\t\t\t\t£{:.2f}'.format(round(self.repayments['interest'], 2)))
        print('  Bad debt recovery:\t\t\t\t£{:.2f}'.format(round(self.repayments['recovery'], 2)))
        print('  Transfer Payment:\t\t\t\t£{:.2f}'.format(round(self.loan_parts['transfer_payment'], 2)))
        print('\t\t\t\t\t\t--------')
        print('  Total incomings:\t\t\t\t£{:.2f}'.format(round(self.repayments['principal'] + self.repayments['interest'] + self.repayments['recovery'] + self.loan_parts['transfer_payment'], 2)))
        print('')
        print('Totals:')
        print('  Monies transferred in to Funding Circle:\t£{:.2f}'.format(round(self.transfers['in'], 2)))
        print('  Monies transferred out of Funding Circle:\t£{:.2f}'.format(round(self.transfers['out'], 2)))
        print('\t\t\t\t\t\t--------')
        print('  Capital difference in account:\t\t£{:.2f}'.format(round(self.transfers['in'] - self.transfers['out'], 2)))
        print('')
        print('  Net interest:\t\t\t\t\t£{:.2f}'.format(round(profit_before_fees, 2)))
        print('   + Bad debt recovery:\t\t\t\t£{:.2f}'.format(round(self.repayments['recovery'], 2)))
        print('   + Transfer Payment:\t\t\t\t£{:.2f}'.format(round(self.loan_parts['transfer_payment'], 2)))
        print('   - Fees paid:\t\t\t\t\t£{:.2f}'.format(round(self.fees, 2)))
        print('\t\t\t\t\t\t--------')
        print('  Monthly profit/loss:\t\t\t\t£{:.2f}'.format(round(profit_before_fees - self.fees + self.repayments['recovery'] + self.loan_parts['transfer_payment'], 2)))
        print('')


def parseAndPrint(filename):
    s = statement(filename)

    s.readFile()
    s.findTransfers()
    s.findLoans()
    s.findLoanParts()
    s.calculateFees()
    s.findRepayments()
    s.printSummary()


def main():
    parser = argparse.ArgumentParser(
        description='Calculate total income from Funding Circle monthly statement.'
    )

    parser.add_argument(
        'file',
        help = 'Path to the monthly statement.',
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print('File "{}" does not exist.'.format(args.file))
        exit(1)

    parseAndPrint(args.file)


if __name__ == "__main__":
    main()
