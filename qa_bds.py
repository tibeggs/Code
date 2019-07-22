# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:07:55 2019

@author: tibeg
"""
import pandas as pd
import math

file="C:/Users/tibeg/Desktop/"
table = "bds_f_sic_release.csv"

data=pd.read_csv(file+table)
data.sort("year2",ascending=1)
p1 = 5
p2 = .05
p3 = 10000
p4 = .8

print(data.head())

list(data)

list(data['sic1'].unique())

def year2yearcomp(data, var, var2, p1=5, p2=5, p3=10000, p4=.8):
    for i in list(data[var].unique()):
        datavar = data.loc[data[var] == i]
        ntm1 = datavar[var2].shift(1)
        nt1 = datavar[var2].shift(-1)
        year2year = datavar[var2].diff()
        abs_year2year = abs(year2year)
        abs_year2yearntm1 = abs_year2year/ntm1
        year2year1 = year2year.shift(-1)
        abs_year2year1 = abs_year2year.shift(-1)
        p75_abs_year2year = abs_year2year.quantile([.75]).item()
        datavar["issue"] = 0
#outlier pararmeter 1
        datavar.loc[abs_year2year < p1*p75_abs_year2year, "issue"]  = +1
#outlier parameter 2
        datavar.loc[abs_year2yearntm1 > p2, "issue"] = +1
#outlier parameter 3
        datavar.loc[abs_year2year > p3, "issue"] = +1
#outlier parameter 4
        #this does not work copysign does not work on a series
        datavar.loc[(math.copysign(1,year2year1) != math.copysign(1,year2year)) and (abs_year2year1 >= abs_year2year), "issue"] = +1
        print(datavar["issue"])

        print("complete")
        
year2yearcomp(data, "sic1", "firms")
    

datasic1 = data.loc[data.sic1 == 70]

year2year = datasic1.firms.diff()

abs_year2year = abs(year2year)

p75_abs_year2year = abs_year2year.quantile([.75]).item()

type(p75_abs_year2year)


data["test"] = -5654

data.test.astype("str").str.find("-")
