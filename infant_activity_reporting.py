#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timedelta
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
            self.rawData = json.load(fh)
            for row in self.rawData:
                self.parse(row)
        fh.close()
        return True

    # Thanks to the SO answer here:
    # https://stackoverflow.com/questions/32723150/rounding-up-to-nearest-30-minutes-in-python
    # for the idea on how to do with datetime object.
    # Note: the mod operation is a python3 operator (doesn't work with py2).
    def _round_timestamp_to_nearest_30(self,timestamp,round_mins=30):
        round_mins = timedelta(minutes=round_mins)
        if( not((datetime.min - timestamp) % round_mins) > (round_mins / 2) ):
            return (timestamp + (datetime.min - timestamp) % round_mins)
        else:
            return (timestamp + (((datetime.min - timestamp) % round_mins) - round_mins))

    def _add_days_to_date(self,date,days):
        return self._date_from_string(date) + timedelta(days=days)

    def _date_from_string(self,date):
        return datetime.strptime(date,'%Y%m%d')

    def _timestamp_from_string(self,date,timestamp):
        return datetime.strptime(date + " " + timestamp,'%Y%m%d %H:%M:%S')

    def _str_date_from_date(self,date_obj):
        return date_obj.strftime('%Y%m%d')

    def _str_timestammp_from_date(self,date_obj):
        return date_obj.strftime('%H%M%S')

    def _buid_time_dict(self,aDict):
        d = {
            'time_start': self._timestamp_from_string(aDict['date'],aDict['time_start']),
            'time_stop': self._timestamp_from_string(aDict['date'],aDict['time_stop']),
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
            self.data[c_date]['sleep'].append(t_dict)

        else:
            if('cry' not in self.data[c_date] ):
                self.data[c_date]['cry'] = list()

            t_dict = self._buid_time_dict(aDict)
            self.data[c_date]['cry'].append(t_dict)

    def getData(self):
        return self.data

    def getDailyData(self,date):
        return self.data[date]

    def getSlidingData(self,startDate,slidingWindow):
        slideData=dict()
        for i in range(slidingWindow):
            current_date=self._add_days_to_date(startDate,i)
            current_date_str=self._str_date_from_date(current_date)
            slideData[current_date_str]=self.getDailyData(current_date_str)
        return slideData

    def getDailyCount(self):
        pass

    def getActivityData(self):
        total_sleep_time=0
        the_number_of_sleeps=0
        posture_duration={}
        total_cry_time=0
        the_number_of_cries=0
        dict_half_hour={}
        if(activity=='sleep'):
            for k,v in self.getSlidingData(date,slidingWindow).items():
                for i in range(len(v['sleep'])):
                    total_sleep_time+=int(v['sleep'][i]['duration'])
                    if(v['sleep'][i]['posture'] not in posture_duration):
                        posture_duration[v['sleep'][i]['posture']]=0
                    posture_duration[v['sleep'][i]['posture']]+=int(v['sleep'][i]['duration'])
                the_number_of_sleeps+=len(v['sleep'])
        else:
            try:
                for k,v in self.getSlidingData(date,slidingWindow).items():

                    for i in range(len(v['cry'])):
                        total_cry_time+=int(v['cry'][i]['duration'])
                    the_number_of_cries+=len(v['cry'])
            except(KeyError):
                pass

        return {'total_sleep_time':total_sleep_time
                ,'the_number_of_sleeps': the_number_of_sleeps
                ,'posture_duration':posture_duration
                ,'total_cry_time':total_cry_time
                ,'the_number_of_cries': the_number_of_cries}

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
    ih_test.readData(file_path="./data/test_data.json",file_type='JSON')
    # print(ih_test.getData())
    # print(ih_test.getDailyData('20170901'))
    print(ih_test.getSlidingData('20170901',3))
    print(ih_test.getActivityData(activity='cry',date='20170901',slidingWindow=3))
    print(ih_test._round_timestamp_to_nearest_30(datetime.now()))


if(__name__ == '__main__'):
    main()
