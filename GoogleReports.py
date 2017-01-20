import json
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.discovery import build
import string


class GoogleReporter:
    client_email = 'YOUR_CLIENT_MAIL'
    json_file = 'YOUR_PRIVATE_KEY.json'
    cloud_storage_bucket = 'pubsite_prod_rev_BUCKET_ID'
    report_to_download = 'financial-stats/subscriptions/FILE_NAME_'
    newSubscriberIndex = 4
    cancelledIndex = 5
    activeSubscriberIndex = 6

    subscribers = 0
    cancellations = 0
    activeSubscribers = 0

    def UpdateReportToDownloadName(self, reportDate):
        self.report_to_download += reportDate + "_device.csv"

    def __init__(self, reportDate):
        self.UpdateReportToDownloadName(reportDate[:-2])
        private_key = json.loads(open(self.json_file).read())['private_key']
        credentials = SignedJwtAssertionCredentials(self.client_email, private_key,
                                                    'https://www.googleapis.com/auth/devstorage.read_only')
        self.storage = build('storage', 'v1', http=credentials.authorize(Http()))
        self.DownloadCsv(reportDate)

    def DownloadCsv(self, date):
        print 'Downloading Google Financial Report (' + date + ')..'
        req = self.storage.objects().get_media(bucket=self.cloud_storage_bucket, object=self.report_to_download).execute()
        response = req.decode(encoding='utf-16')
        response = string.split(repr(response), '\\n')

        self.activeSubscribers = 0
        self.cancellations = 0
        self.subscribers = 0
        #print date[-2:]

        for row in response[1:]:
            line = string.split(row, ',')
            if line[0].__str__().endswith(date[-2:]):
                self.activeSubscribers += int(line[self.activeSubscriberIndex])
                self.subscribers += int(line[self.newSubscriberIndex])
                self.cancellations += int(line[self.cancelledIndex])
        #print self.activeSubscribers.__str__() + ", " + self.subscribers.__str__() + ", " + self.cancelations.__str__()
        # with open(os.path.join("", "testFile.csv"), "wb") as wer:
        #     wer.write(req)

        # print 'Download Complete!'
