#! /opt/local/bin/python

import sys
import matplotlib.pyplot as plt
from pylab import *
import datetime as dt
import numpy as np

from qstkutil import DataAccess as da
from qstkutil import qsdateutil as du
from qstkutil import tsutil as tsu
import pandas

def main(startport,orderfile,output):
    # read in the order book
    data = np.loadtxt(orderfile,dtype='I,I,I,S5,S4,I',delimiter=',')
    ordersyms = []
    order = []
    amount = []
    orderdate =[]
    exdate = []
    for i in data:
        ordersyms.append(i[3])
        order.append(i[4])
        amount.append(i[5])
        exdate.append(dt.date(i[0],i[1],i[2]))
    exdate=np.array(exdate)
    # build portfolio
    port = {}
    for stock in ordersyms:
        port.update({stock:0})
    stocks = port.keys()

    # check the validity
    dataobj = da.DataAccess('Yahoo')
    all_symbols = dataobj.get_all_symbols()
    intersectsyms = list(set(all_symbols) & set(stocks))
    bydsyms = []
    if size(intersectsyms) < size(stocks):
        badsyms = list(set(stocks) - set(intersectsyms))
        print "!! warning: portforlio contains symbols that do not exist:"
        print badsyms
        print "exiting now"
        exit()

    # looping date
    startday = dt.datetime(2011,1,1)
    endday = dt.datetime(2011,12,31)
    timeofday = dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
    close = dataobj.get_data(timestamps,stocks,"close")
        # fill NAN in array
    close = (close.fillna(method='ffill')).fillna(method='backfill')

    # set the balance of the portfolio
    port.update({'cash':startport})
    # set output
    f = open(output,'w')

    balance = startport
    for dayid,day in enumerate(timestamps):
        # excute order
        if (day.date() in exdate):
            id = np.where(exdate == day.date())[0]
            for i in id:
                stockid = stocks.index(ordersyms[i])
                print 'on day',close.index[dayid].date(),'stock',close.columns[stockid],
                if (order[i] == 'Buy'): # buy stock
                    # print ' - ',order[i],amount[i],ordersyms[i],exdate[i],close.values[dayid,stockid]
                    restamount = port[ordersyms[i]]+amount[i]
                    cash = port['cash']-amount[i]*close.values[dayid,stockid]
                elif (order[i] == 'Sell'): # sell stock
                    # print ' - ',order[i],amount[i],ordersyms[i],exdate[i]
                    restamount = port[ordersyms[i]]-amount[i]
                    cash = port['cash']+amount[i]*close.values[dayid,stockid]
                else:
                    print "!! wrong order:',order[i]"
                    print "exiting now!!"
                    exit()
                # record change
                port.update({ordersyms[i]:restamount})
                port.update({'cash':cash})
        # record balance
        balance = 0
        for stockid,stock in enumerate(stocks):
            balance += close.values[dayid,stockid]*port[stock]
        balance += port['cash']
        # output
        #print day, balance
        output = str(day.year)+','+str(day.month)+','+str(day.day)+','+str(balance)+'\n'
        f.write(output)
    f.close()

if __name__ == "__main__":
    main(np.float_(sys.argv[1]),sys.argv[2],sys.argv[3])
