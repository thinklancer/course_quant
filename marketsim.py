#! /opt/local/bin/python

import sys
import matplotlib.pyplot as plt
from pylab import *
import datetime as dt

from qstkutil import DataAccess as da
from qstkutil import qsdateutil as du
from qstkutil import tsutil as tsu


def main(inital,orderfile,output):
    # read in the order book
    data = np.loadtxt(orderfile,dtype='I,I,I,S5,S4,I',delimiter=',')
    ordersyms = []
    order = []
    amount = []
    orderdate =[]
    for i in data:
        ordersyms.append(i[3])
        order.append(i[4])
        amount.append(i[5])
        
    # build portfolio
    port = {}
    for stock in ordersyms:
        port.update({stock:0})
    
    # check the validity
    dataobj = da.DataAccess('Yahoo')
    all_symbols = dataobj.get_all_symbols()
    intersectsyms = list(set(all_symbols) & set(port.keys))
    bydsyms = []
    if size(intersectsyms) < size(port.keys):
        badsyms = list(set(port.keys) - set(intersectsyms))
        print "warning: portforlio contains symbols that do not exist:"
        print badsyms
        exit()

    # set the balance of the portfolio
    print type(initial)
    port.update({"cash":initial})

    # looping date
    startday = dt.datetime(2011,1,1)
    endday = dt.datetime(2011,12,31)
    timeofday = dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
    close = dataobj.get_data(timestamps,port.keys,"close")

    # excute order

    # record balance

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
