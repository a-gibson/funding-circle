#!/usr/bin/python3

import argparse
import calendar
import os.path
import re

import parse_statement


def removeNonCsvFiles(files):
    for f in reversed(files):
        if os.path.splitext(f)[1] == ".csv":
            print('Found CSV file: "{}"'.format(f))
        else:
            files.remove(f)


def printHeading(filename):
    search_term = 'statement_(?P<year>20\d\d)-(?P<month>\d\d)_'

    result = re.match(search_term, filename)
    month_name = calendar.month_name[int(result.group('month'))]
    print("====================  {}  {}  ====================".format(result.group('year'), month_name))


def printTail():
    print("")
    print("================================================================================")
    print("")


def parseFiles(path):
    file_list = os.listdir(path)
    file_list.sort()

    removeNonCsvFiles(file_list)

    for f in file_list:
        full_file_path = path + '/' + f
        printHeading(f)
        parse_statement.parseAndPrint(full_file_path)
        #printTail()


def main():
    parser = argparse.ArgumentParser(description='Calculate total income from multiple Funding Circle monthly statements.')

    parser.add_argument(
        '--path',
        default='.',
        help='Path to the monthly statement.')

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print('Path "{}" does not exist.'.format(args.path))
        exit(1)

    parseFiles(args.path)

if __name__ == "__main__":
    main()
