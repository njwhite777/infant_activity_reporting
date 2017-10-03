#!/usr/bin/python
import csv
import json
import datetime
from csv import DictReader
from collections import OrderedDict

class InfantHealthMS(object):

    def __init__(self):
        self.rawData = list()
        self.data = OrderedDict()

    def readData(self,file_path,file_type='CSV'):

        try:
            fh = open(file_path,'r')
        except Exception as e:
            print(e)
            return False

        if( file_type == 'CSV' ):
            dr = DictReader(fh)
            for row in dr:
                self.rawData.append(row)
                self.parse(row)

        elif( file_type == 'JSON' ):

            pass
        fh.close()
        return True

    def _add_days_to_date(self,date,days):
        return self._date_from_string(date) + datetime.timedelta(days=days)

    def _date_from_string(self,date):
        return datetime.strptime(date,'%Y%m%d')

    def _timestamp_from_string(self,timestamp):
        return datetime.strptime(timestamp,'%H:%M:%S')

    def _buid_time_dict(self,aDict):
        d = {
            'time_start': datetime.strptime(aDict['date'] + " " + aDict['time_start'], '%Y%m%d %H:%M:%S'),
            'time_end': datetime.strptime(aDict['date'] + " " + aDict['time_end'], '%Y%m%d %H:%M:%S'),
            'duration': aDict['duration']
        }
        if('posture' in aDict):
            d['posture'] = aDict['posture']

        return d

    def parse(self,aDict,tRow=None):

        c_date = aDict['date']

        if(c_date not in self.data):
            self.data[c_date] = dict()


        if( 'posture' in aDict ):
            if('sleep' not in self.data[c_date] ):
                self.data[c_date]['sleep'] = list()

            t_dict = self._buid_time_dict(aDict)
            self.data[c_date]['posture'].append(t_dict)

        elif( 'cry' in aDict ):
            if('cry' not in self.data[c_date] ):
                self.data[c_date]['cry'] = list()

            t_dict = self._buid_time_dict(aDict)
            self.data[c_date]['posture'].append(t_dict)

    def getData(self):
        return self.data

    def getDailyData(self,date):
        return self.data[date]

    def getSlidingData(self,startDate,slidingWindow):
        slideData=dict()
        for i in range(slidingWindow):
            current_date=self._add_days_to_date(startDate,i)
            current_date_str=current_date.tostring
            slideData[current_date_str]=self.getDailyData(current_date_str)

    def getDailyCount(self):
        pass

    def getActivityData(self):
        pass

    def generateReport(self):
        pass


class InfantSleepMS(InfantHealthMS):

    def __init__(self):
        InfantHealthMS.__init__(self)
        pass

    def getSleepCount(self):
        pass

    def getSleepTime(self):
        pass

    def getSleepTimeInPostuer(self):
        pass

    def getSleepSlot(self):
        pass


class InfantCryMS(InfantHealthMS):

    def __init__(self):
        InfantHealthMS.__init__(self)
        pass

    def getCryCount(self):
        pass

    def getCryTime(self):
        pass

    def getCryTimeInPostuer(self):
        pass

    def getCrySlot(self):
        pass

def main():
    ih_test = InfantHealthMS()


if(__name__ == '__main__'):
    main()
