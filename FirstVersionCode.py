#!/usr/bin/python
import csv
import json
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
            # TODO: implement JSON import
            pass
        fh.close()
        return True

    def _buid_time_dict(self):
        pass

    def parse(self,aDict,tRow=None):

        c_date = aDict['date']

        if(c_date not in self.data):
            self.data[c_date] = dict()


        if( 'posture' in aDict ):
            if('posture' not in self.data[c_date] ):
                self.data[c_date]['posture'] = list()

            # t_dict =
            # self.data[c_date]['posture'].append()

        elif( 'cry' in aDict ):
            if('cry' not in self.data[c_date] ):
                self.data[c_date]['cry'] = list()

        pass

    def getDailyData(self):
        pass

    def getSlidingData(self):
        pass

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
