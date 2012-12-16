#! /opt/local/bin/python

## @package homework 3
#  Analyze the performance of a portfolio
import qstkutil.qsdateutil as du
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import pandas

import datetime as dt

import numpy as np
from pylab import *
import matplotlib.pyplot as plt


def main(ifile,index):
    # access the historical brenchmark
    # print "Access the historical data of ",index
    symbol = [index]
    startday = dt.datetime(2008,1,1)
    endday = dt.datetime(2009,12,31)
    timeofday = dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)

    dataobj = da.DataAccess('Yahoo')
    close_price = dataobj.get_data(timestamps,symbol,"close")
    
    # import portfolio performance
    port = np.loadtxt(ifile,delimiter=',')
    portprice = port[:,3]
    portprice = portprice/portprice[0]
    datesdat = np.int_(port[:,0:3])
    dates = []
    for i in range(0,datesdat.shape[0]):
        dates.append(dt.date(datesdat[i,0],datesdat[i,1],datesdat[i,2]))
    # plot the result
    plt.clf()
    plt.plot(dates,portprice)
    newtimestamps = close_price.index
    pricedat = close_price.values/close_price.values[0]
    plt.plot(newtimestamps,pricedat)
    plt.legend(['portfolio',symbol])
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    savefig('adjustedclose.pdf',format='pdf')
    # analyze the return
    print 'total return',(portprice[-1]-1)*100.
    # analyze stddev
    meanreturn = np.mean(portprice-1)
    stddev = np.std(portprice)
    print 'stddev:',stddev*100
    # sharpe ratio
    return0 = np.mean(pricedat-1)
    sharpe = (meanreturn-return0)/stddev
    print 'sharpe ratio:',sharpe


if __name__ == "__main__":
    import sys
    main(sys.argv[1],sys.argv[2])