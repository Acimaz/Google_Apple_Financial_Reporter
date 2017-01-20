from subprocess import *
import gzip
import string
import os
import time
import ApplePythonReporter

class ApplePythonReport:
    vendorId = YOUR_VENDOR_ID
    userId = 'YOUR_ITUNES_CONNECT_ACCOUNT_MAIL'
    password = 'ITUNES_CONNECT_PASSWORD'
    account = 'ACCOUNT_ID'
    mode = 'Robot.XML'
    dateType = 'Daily'
    eventIndex = 1
    activeSubscriberIndex = 16
    quantityIndex = 25

    subscribers = 0
    cancellations = 0
    activeSubscribers = 0
    maxAttempts = 5

    def __init__(self, reportDate):
        self.DownloadSubscriptionEventReport(reportDate)
        self.DownloadSubscriptionReport(reportDate)
        self.FetchSubscriptionEventData(reportDate)
        self.FetchSubscriptionData(reportDate)
        self.CleanUp(reportDate)

    def DownloadSubscriptionEventReport(self, date):
        print 'Downloading Apple Financial Report for Subscriptions (' + date + ')..'
        credentials = (self.userId, self.password, self.account, self.mode)
        command = 'Sales.getReport, {0},SubscriptionEvent,Summary,{1},{2}'.format(self.vendorId, self.dateType, date)
        try:
            ApplePythonReporter.output_result(ApplePythonReporter.post_request(ApplePythonReporter.ENDPOINT_SALES,
                                                                           credentials, command))
        except Exception:
            pass
        #return iter(p.stdout.readline, b'')

    def DownloadSubscriptionReport(self, date):
        print 'Downloading Apple Financial Report for Active Users (' + date + ')..'
        credentials = (self.userId, self.password, self.account, self.mode)
        command = 'Sales.getReport, {0},Subscription,Summary,{1},{2}'.format(self.vendorId, self.dateType, date)
        try:
            ApplePythonReporter.output_result(ApplePythonReporter.post_request(ApplePythonReporter.ENDPOINT_SALES,
                                                                           credentials, command))
        except:
            pass
        #return iter(p.stdout.readline, b'')

    #Uncompress and extract needed values (cancellations and new subscribers)
    def FetchSubscriptionEventData(self, date):
        fileName = 'Subscription_Event_'+self.vendorId+'_' + date + '.txt'
        attempts = 0
        while not os.path.isfile(fileName):
            if(attempts >= self.maxAttempts):
                break
            attempts += 1
            time.sleep(1)

        if os.path.isfile(fileName):
            print 'Fetching SubscriptionEvents..'
            with open(fileName, 'rb') as inF:
                text = inF.read().splitlines()
                for row in text[1:]:
                    line = string.split(row, '\t')
                    # print line[self.eventIndex].__str__()
                    if line[0].__str__().endswith(date[-2:]):
                        if line[self.eventIndex] == 'Cancel':
                            self.cancellations += int(line[self.quantityIndex])
                        if line[self.eventIndex] == 'Subscribe':
                            self.subscribers += int(line[self.quantityIndex])
        else:
            print 'SubscriptionEvent: There were no sales for the date specified'

    # Uncompress and extract needed values (active users)
    def FetchSubscriptionData(self, date):
        fileName = 'Subscription_'+self.vendorId+'_' + date + '.txt'
        attempts = 0
        while not os.path.isfile(fileName):
            if (attempts >= self.maxAttempts):
                break
            attempts += 1
            time.sleep(1)

        if os.path.isfile(fileName):
            print 'Fetching Subscriptions..'
            with open(fileName, 'rb') as inF:
                text = inF.read().splitlines()
                for row in text[1:]:
                    line = string.split(row, '\t')
                    # print line[0].__str__()
                    self.activeSubscribers += int(line[self.activeSubscriberIndex])
        else:
            print 'Subscription: There were no sales for the date specified'

    def CleanUp(self, date):
        if os.path.isfile('Subscription_'+self.vendorId+'_' + date + '.txt'):
            os.remove('Subscription_'+self.vendorId+'_' + date + '.txt')
        else:
            print 'Subscription_'+self.vendorId+'_' + date + '.txt doesnt exist: Maybe there were no Sales at the specified date'
        if os.path.isfile('Subscription_Event_'+self.vendorId+'_' + date + '.txt'):
            os.remove('Subscription_Event_'+self.vendorId+'_' + date + '.txt')
        else:
            print 'Subscription_Event_'+self.vendorId+'_' + date + '.txt doesnt exist: Maybe there were no Sales at the specified date'