'''
   make order based on strategy
'''

import pandas
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep

#closefield = "actual_close"
closefield = "close"
volumefield = "volume"

def findEvents(symbols, startday,endday, marketSymbol):
	# Reading the Data for the list of Symbols.
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(startday,endday,timeofday)
	dataobj = da.DataAccess('Yahoo')

	# Reading the Data
	close = dataobj.get_data(timestamps, symbols, closefield)
	    
	np_eventmat = copy.deepcopy(close)
	for sym in symbols:
		for time in timestamps:
			np_eventmat[sym][time]=np.NAN
	f = open('order.csv','w')
	totaldays = len(timestamps)
	for symbol in symbols:
		for i in range(1,totaldays):
			if close[symbol][i-1] >= 6. and close[symbol][i] < 6. :
				#print timestamps[i].year,',',timestamps[i].month,',',timestamps[i].day,',Buy,',symbol,',100'
				soutput = str(timestamps[i].year)+','+str(timestamps[i].month)+','+str(timestamps[i].day)+','+symbol+',Buy,100\n'
				f.write(soutput)
				j = i+5
				if j >= totaldays:
					j = totaldays-1
				soutput = str(timestamps[j].year)+','+str(timestamps[j].month)+','+str(timestamps[j].day)+','+symbol+',Sell,100\n'
                		f.write(soutput)
	f.close()

if __name__ == "__main__":
    dataobj = da.DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list("sp5002012")
    symbols.append('SPY')

    startday = dt.datetime(2008,1,1)
    endday = dt.datetime(2009,12,31)
    findEvents(symbols,startday,endday,marketSymbol='SPY')


