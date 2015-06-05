import datetime
from datetime import date

enddate = None
startdate = 'May 15, 2014'
time_format = '%b %d, %Y'

if __name__ == '__main__':
        
    dates = [startdate, enddate] #Quick check for correct date format
    for date_ in dates:
        if date_ != None: 
            try:
                datetime.datetime.strptime(date_, time_format)
            except:
                print "Date format cobflict"
                
    if enddate == None:
        enddate = date(date.today().year, date.today().month, date.today().day).strftime(time_format)
        
    print enddate, startdate