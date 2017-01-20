from datetime import date

from datetime import timedelta


class ReportDate:

    def SetTime(self, daysBefore):
        self.year = (date.today() - timedelta(days=daysBefore)).year
        self.month = (date.today() - timedelta(days=daysBefore)).strftime('%m')
        self.day = (date.today() - timedelta(days=daysBefore)).strftime('%d')

    def ToString(self):
        return "{0}-{1}-{2}".format(self.year, self.month, self.day)

    def __init__(self, daysBefore):
        self.year = (date.today() - timedelta(days = daysBefore)).year
        self.month = (date.today() - timedelta(days=daysBefore)).strftime('%m')
        self.day = (date.today() - timedelta(days=daysBefore)).strftime('%d')

