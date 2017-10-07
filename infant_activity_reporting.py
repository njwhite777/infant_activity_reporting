#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timedelta
from csv import DictReader
from collections import OrderedDict
from prettytable import PrettyTable

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
    def _round_timestamp_to_nearest_interval(self,timestamp,round_mins=30):
        round_mins = timedelta(minutes=round_mins)
        if( not((datetime.min - timestamp) % round_mins) > (round_mins / 2) ):
            return self._str_timestamp_from_date(timestamp + (datetime.min - timestamp) % round_mins)  #Convert Datetime type to Str
        else:
            return self._str_timestamp_from_date(timestamp + (((datetime.min - timestamp) % round_mins) - round_mins)) #Convert Datetime type to Str

    def _add_days_to_date(self,date,days):
        return self._date_from_string(date) + timedelta(days=days)
        
    def _subtract_days_from_date(self,date,days):
        return self._date_from_string(date) - timedelta(days=days)

    def _date_from_string(self,date):
        return datetime.strptime(date,'%Y%m%d')

    def _timestamp_from_string(self,date,timestamp):
        return datetime.strptime(date + " " + timestamp,'%Y%m%d %H:%M:%S')

    def _str_date_from_date(self,date_obj):
        return date_obj.strftime('%Y%m%d')

    def _str_timestamp_from_date(self,date_obj):
        return date_obj.strftime('%H:%M:%S')

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

    # def getDailyData(self,date):
    #     return self.data[date]

    def getDailyData(self,date):
        return self.getActivityData(date,1)

    def getSlidingData(self,startDate,slidingWindow):
        slideData=dict()
        for i in range(slidingWindow):
            current_date=self._add_days_to_date(startDate,i)
            current_date_str=self._str_date_from_date(current_date)
            if( current_date_str in self.data):
                slideData[current_date_str]=self.data[current_date_str]
        return slideData

    def getDailyCount(self):
        pass

    def getActivityData(self,activity,date,slidingWindow):
        total_time          = 0
        count_of_activity   = 0
        posture_duration    = {}
        dict_half_hour      = {}
        likely_event_start  = []

        event_threshold     = 0
        if(slidingWindow == 7):
            event_threshold = 3
        elif(slidingWindow in [28,29,30,31]):
            event_threshold = 21

        sd = self.getSlidingData(date,slidingWindow).items()
        
        
        # if(activity=='sleep'):
            
        for k,v in sd:
            
            if(activity not in v):
                continue
                
            for i in range( len(v[activity]) ):
                total_time+=int(v[ activity ][i]['duration'])
                
                if( activity == 'sleep' and v[ activity ][i]['posture'] not in posture_duration):
                    posture_duration[v['sleep'][i]['posture']]=0

                a_dict = v[activity][i]
                st_timestamp = self._round_timestamp_to_nearest_interval(v[ activity ][ i ][ 'time_start' ])

                if(st_timestamp not in dict_half_hour):
                    dict_half_hour[ st_timestamp ]={ 'count' : 0, 'dates' : [] }

                dict_half_hour[ st_timestamp ][ 'count' ] += 1
                dict_half_hour[ st_timestamp ][ 'dates' ].append(k)
                
                if(dict_half_hour[ st_timestamp ][ 'count' ] >= event_threshold):
                    if(st_timestamp not in likely_event_start):
                        likely_event_start.append(st_timestamp)

                
                if( activity == 'sleep' ):
                    posture_duration[ a_dict['posture'] ] += int( a_dict['duration'] )

            count_of_activity += len(v[activity])

        return {
                # 'total_sleep_time':total_sleep_time,
                # 'total_cry_time':total_cry_time,
                # 'the_number_of_sleeps': the_number_of_sleeps,
                # 'the_number_of_cries': the_number_of_cries,
                    'total_time'         :  total_time,
                    'count_of_activity'  :  count_of_activity,
                    'posture_duration'   :  posture_duration,
                    'dict_half_hour'     :  dict_half_hour,
                    'likely_event_start' :  likely_event_start
                }

    def generateReport(self):
        pass
    
    def report_from_current_date(self,duration='week',month_window=30):
        c_time = datetime.now()
        date = self._str_date_from_date(c_time)
        if(duration == 'week'):
            st_date = self._str_date_from_date(self._subtract_days_from_date(date,8))
            self.generateReport(st_date,7)
        if(duration == 'month'):
            st_date = self._str_date_from_date(self._subtract_days_from_date(date,month_window+1))
            self.generateReport(st_date,month_window)

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

    def getActivityData(self,date,slidingWindow):
        return super().getActivityData(activity='sleep',date=date,slidingWindow=slidingWindow)

    def generateReport(self,date,slidingWindow):
        
        print("Sleep report for {} through {}".format(date,self._str_date_from_date(self._add_days_to_date(date,7))))
        print("==============================================================================================")
        data = None
        if( slidingWindow == 1 ):
            data = self.getDailyData(date)
            pt = PrettyTable()
            pt2 = PrettyTable()
            pt.field_names = ["Number of Naps","Total Sleep Time"]
            pt.add_row( [data['count_of_activity'],data['total_time']] )
            pt2.field_names = data['posture_duration'].keys()
            pt2.add_row(data['posture_duration'].values())
            print("Basic stats:")
            print(pt)
            print("Duration in Sleep Posture:")
            print(pt2)
            print()
        else:
            data = self.getActivityData(date,slidingWindow=slidingWindow)
            pt = PrettyTable()
            pt1 = PrettyTable()
            pt2 = PrettyTable()
            pt.field_names = ["Number of Naps","Total Sleep Time"]
            pt.add_row( [data['count_of_activity'],data['total_time']] )
            pt1.field_names = ['Time','Count','Dates']
            for hhi,hh_dict in data['dict_half_hour'].items():
                pt1.add_row([hhi,hh_dict['count'],hh_dict['dates']])
            print("Sleep Start Times:")
            print(pt1)
            print("Basic stats:")
            print(pt)
            if(not(data['posture_duration'] == {})):
                print("Duration in Sleep Posture:")
                pt2.field_names = data['posture_duration'].keys()
                pt2.add_row(data['posture_duration'].values())
                print(pt2)
            if( len(data['likely_event_start']) > 0 ):
                print("Most likely sleep starting times",data['likely_event_start'])
            print()
            
            

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

    def getActivityData(self,date,slidingWindow):
        t_dict = super().getActivityData(activity='cry',date=date,slidingWindow=slidingWindow)
        del t_dict['posture_duration']
        return t_dict

    def generateReport(self,date,slidingWindow):

        data = None
        print()
        print("Cry report for {} through {}".format(date,self._str_date_from_date(self._add_days_to_date(date,7))))
        print("==============================================================================================")
        if( slidingWindow == 1 ):
            data = self.getDailyData(date)
            pt = PrettyTable()
            pt.field_names = ["Number of Cries","Total Cry Time"]
            pt.add_row( [data['count_of_activity'],data['total_time']] )
            print(pt)
            print()
        else:
            data = self.getActivityData(date,slidingWindow=slidingWindow)
            pt = PrettyTable()
            pt1 = PrettyTable()
            pt.field_names = ["Number of Cries","Total Cry Time"]
            pt.add_row( [data['count_of_activity'],data['total_time']] )
            pt1.field_names = ['Time','Count','Dates']
            for hhi,hh_dict in data['dict_half_hour'].items():
                pt1.add_row([hhi,hh_dict['count'],hh_dict['dates']])
            print("Cry Start Times:")
            print(pt1)
            print("Basic stats:")
            print(pt)
            if( len(data['likely_event_start']) > 0 ):
                print("Most likely cry starting times",data['likely_event_start'])


def main():
    #
    ih_test = InfantHealthMS()
    ih_test.readData(file_path="./data/test_data.json",file_type='JSON')
    #
    ihc_test = InfantCryMS()
    ihc_test.readData(file_path="./data/test_data.json",file_type='JSON')
    #
    ihs_test = InfantSleepMS()
    ihs_test.readData(file_path="./data/test_data.json",file_type='JSON')


    print()
    ihs_test.report_from_current_date(duration='week')
    print()
    ihs_test.report_from_current_date(duration='month')
    
    print()
    ihc_test.report_from_current_date(duration='week')
    print()
    ihc_test.report_from_current_date(duration='month')


if(__name__ == '__main__'):
    main()
