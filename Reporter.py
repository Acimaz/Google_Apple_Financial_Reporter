# Reporting tool for querying Sales- and Financial Reports from iTunes Connect and Google Developer Console
#
# This tool can be used to download financial reports from both Google and Apple
# for the app of your choice (of course i assume that you are the owner of this app)
#
# Copyright (c) 2017 Ayhan Sakarya, Kaasa health GmbH  <ayhan.sakarya@kaasahealth.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import getopt
import csv
import os
from Utility import ReportDate
from GoogleReports import GoogleReporter
from AppleReporter import ApplePythonReport

currentDate = None
googleReporter = None
appleReporter = None


def UpdateMainReportFile(date):
    global googleReporter
    global appleReporter
    fileExists = os.path.isfile('financialReport.csv')
    with open('financialReport.csv', 'r') as csvFileRead:
        print 'Updating financialReport.csv..'
        dateExists = False
        deleteFirstRows = False
        headers = ['Date', 'Platform', 'newSubscriptions', 'cancelledSubscriptions', 'activeSubscriptions']
        reader = csv.DictReader(csvFileRead, delimiter=',')
        #print 'Length: ' + len(list(reader)).__str__()
        readerList = list(reader)
        csvFileRead.seek(0)
        listLength = 0
        for line in reader:
            listLength += 1
            if date == line['Date']:
                dateExists = True

        if listLength > 118:        #118 because we want to have the data of the past 60 days and we have 2 rows for each day (google, apple)
            deleteFirstRows = True
        csvFileRead.seek(0)
        with open('financialReport.csv', 'w') as csvFileWriter:
            writer = csv.DictWriter(csvFileWriter, delimiter=',', lineterminator='\n', fieldnames=headers)

            writer.writeheader()
            replaced = False
            startIndex = 2 if deleteFirstRows else 0
            for line in readerList[startIndex:]:
                if date == line['Date']:
                    if line['Platform'] == 'Apple':
                        writer.writerow(
                            {'Date': date, 'Platform': 'Apple', 'newSubscriptions': appleReporter.subscribers,
                             'cancelledSubscriptions': appleReporter.cancellations,
                             'activeSubscriptions': appleReporter.activeSubscribers})
                    if line['Platform'] == 'Google':
                        writer.writerow(
                            {'Date': date, 'Platform': 'Google', 'newSubscriptions': googleReporter.subscribers,
                             'cancelledSubscriptions': googleReporter.cancellations,
                             'activeSubscriptions': googleReporter.activeSubscribers})
                    replaced = True
                else:
                    writer.writerow(line)

            if not replaced:
                writer.writerow(
                    {'Date': date, 'Platform': 'Apple', 'newSubscriptions': appleReporter.subscribers,
                     'cancelledSubscriptions': appleReporter.cancellations,
                     'activeSubscriptions': appleReporter.activeSubscribers})
                writer.writerow(
                    {'Date': date, 'Platform': 'Google', 'newSubscriptions': googleReporter.subscribers,
                     'cancelledSubscriptions': googleReporter.cancellations,
                     'activeSubscriptions': googleReporter.activeSubscribers})


def main(argv):
    global currentDate
    global googleReporter
    global appleReporter
    try:
        opts, args = getopt.getopt(argv, "d:", ["days="])
    except getopt.GetoptError:
        print 'Reporter.py -d <daysBefore>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--days"):
            currentDate = ReportDate(int(arg))

    print 'Downloading financial reports for ' + currentDate.ToString() + "..."
    googleReporter = GoogleReporter(
        currentDate.year.__str__() + currentDate.month.__str__() + currentDate.day.__str__())
    appleReporter = ApplePythonReport(currentDate.year.__str__() + currentDate.month.__str__() + currentDate.day.__str__())
    # print '\nGoogle\nSubscribers: ' + googleReporter.subscribers.__str__() + ' Cancellations: ' + googleReporter.cancellations.__str__() + ' Active Users: ' + googleReporter.activeSubscribers.__str__()
    # print 'Apple\nSubscribers: ' + appleReporter.subscribers.__str__() + ' Cancellations: ' + appleReporter.cancellations.__str__() + ' Active Users: ' + appleReporter.activeSubscribers.__str__()
    UpdateMainReportFile(currentDate.year.__str__() + '-' + currentDate.month.__str__() + '-' + currentDate.day.__str__())
    print 'Financial Reports are now up to date!\n'

if __name__ == "__main__":
    main(sys.argv[1:])
