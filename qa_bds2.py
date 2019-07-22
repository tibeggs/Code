# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:47:26 2019

@author: beggs005
"""

# -*- coding: utf-8 -*-

"""

Created on Wed Apr 10 10:05:36 2019



@author: beggs005

"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import time
from tkinter import *

master = Tk()

variable = StringVar(master)
variable.set("one")
w = OptionMenu(master, variable,"one", "two","three")
w.pack()

def close_window(): 
    master.destroy()
frame = Frame(master)
frame.pack() 
button = Button (frame, text = "Good-bye.", command = close_window)
button.pack()

mainloop()

print(variable.get())

start_time= time.time()

#read in data table
#ddirectory = "/lbd/bitsi/ewdwork/datatables/"
ddirectory = "C:/Users/tibeg/Documents/datatables"
files = [f for f in os.listdir(ddirectory) if os.path.isfile(os.path.join(ddirectory,f))]
#files = ["bds_f_szmsa_release_outliers.csv"]
print(files)
#set parameters
p1 = 5
p2 = .05
p3 = 10000
p4 = .8

def q3(x):
    return x.quantile(.75)

def spikefunction2(subset,var,a,j,cvar1="",cvar2=""):
    pd.options.mode.chained_assignment = 'raise'        
    subset =subset.assign(ntm1=subset[var].shift(1))        
    subset.loc[:,"ntp1"] = subset[var].shift(-1)        
    subset.loc[:,"ntp2"] = subset[var].shift(-2)        
    subset.loc[:,"year2year"] = subset[var]-subset["ntm1"]        
    subset.loc[:,"year2yearm1"] =subset["year2year"] .shift(1)        
    subset.loc[:,"year2yearp1"] =subset["year2year"] .shift(-1)        
    subset.loc[:,"year2yearp2"] =subset["year2year"] .shift(-2)        
    subset.loc[:,"abs_year2year"] = abs(subset["year2year"])        
    subset.loc[:,"abs_year2yearp1"] = subset["abs_year2year"].shift(-1)        
    subset.loc[:,"abs_year2yearm1"] = subset["abs_year2year"].shift(1)        
    subset.loc[:,"abs_year2yearp2"] = subset["abs_year2year"].shift(-2)              
    subset.loc[:,"sc"] = 0
    subset.loc[:,"sf"] = 0        
    
    f = {'abs_year2year': [q3]}
    q75=subset[["abs_year2year",cvar1,cvar2]].groupby([cvar1,cvar2]).agg(f).reset_index()
    #!cvarref
    q75.columns = [cvar1,cvar2,"q3"]
    #!cvarref
    subset=subset.merge(q75, on=[cvar1,cvar2])

    
#    p75_abs_year2year = subset["abs_year2year"].quantile([.75]).item()  
            
    #outlier parameters        
    subset.loc[:,"op"] = 0        
    subset.loc[subset["abs_year2year"] > p1*subset["q3"], "op"] +=1        
    subset.loc[(subset["ntm1"] !=0) & (subset["abs_year2year"]/subset["ntm1"] > p2), "op"] += 1        
    subset.loc[subset["ntm1"] == 0, "op"] += 1        
    subset.loc[subset["abs_year2year"] > p3, "op"] += 1        
    subset.loc[subset["year2year"]>=0, "sc"] = 1        
    subset.loc[subset["year2yearp1"]>=0, "sf"] = 1        
    subset.loc[(subset["sc"] != subset["sf"]) & (subset["abs_year2yearp1"] >= subset["abs_year2year"]*p4), "op" ] += 1                      
    
    #special rules for first and last
    subset.loc[:,"Last"] = 0      
    #!cvarref    
    last_row_index = subset.groupby([cvar1,cvar2]).tail(1).index.values             
    subset.loc[last_row_index, "Last"] = 1        
    subset.loc[last_row_index, "op"] = 0                                
    subset.loc[:,"First"] = 0   
    #!cvarref
    first_row_index = subset.groupby([cvar1,cvar2]).head(1).index.values             
    subset.loc[first_row_index, "First"] = 1        
    subset.loc[first_row_index, "op"] = 0        
            
    #first adjustments
    subset.loc[(subset["abs_year2yearp1"] > p1*subset["q3"]) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset[var] !=0) & (subset["abs_year2yearp1"]/subset[var] > p2) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset[var] ==0) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset["abs_year2yearp1"] > p3) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset["year2yearp1"]>=0) & (subset["First"] == 1), "sc"] = 1        
    subset.loc[(subset["year2yearp2"]>=0) & (subset["First"] == 1), "sf"] = 1        
    subset.loc[(subset["sc"] == subset["sf"]) & (subset["First"] == 1), "op" ] += 1        
    subset.loc[(subset["sc"] != subset["sf"]) & (subset["First"] != 1) & (subset["abs_year2yearp2"] < subset["abs_year2yearp1"]*p4) & (subset["First"] == 1), "op" ] += 1
    
    #last adjustments
    subset.loc[(subset["abs_year2year"] > p1*subset["q3"]) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["ntm1"] !=0) & (subset["abs_year2year"]/subset["ntm1"] > p2) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["ntm1"] ==0) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["abs_year2year"] > p3) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["year2year"]>=0) & (subset["Last"] == 1), "sc"] = 1        
    subset.loc[(subset["year2yearm1"]>=0) & (subset["Last"] == 1), "sf"] = 1        
    subset.loc[(subset["sc"] == subset["sf"]) & (subset["Last"] == 1), "op" ] += 1        
    subset.loc[(subset["sc"] != subset["sf"]) & (subset["Last"] != 1) & (subset["abs_year2yearm1"] < subset["abs_year2year"]*p4) & (subset["Last"] == 1), "op" ] += 1
    
    #special rules
    #!cvarref
    if cvar1 == "fage4" or cvar2 == "fage4":
        subset.loc[(subset[cvar2]=="g) 6 to 10") & (subset["year2"]<=1987), "op"]=-1
        subset.loc[(subset[cvar2]=="h) 11 to 15") & (subset["year2"]<=1992), "op"]=-1
        subset.loc[(subset[cvar2]=="i) 16 to 20") & (subset["year2"]<=1997), "op"]=-1 
        subset.loc[(subset[cvar2]=="j) 21 to 25") & (subset["year2"]<=2002), "op"]=-1                
    
    #check for outliers
    subset.loc[:,"spike"]=0
    subset.loc[subset["op"]>3, "spike"]=1
    #!cvarref
    spikesum = subset[[cvar1,cvar2,"spike"]].groupby([cvar1,cvar2]).sum().reset_index()
    spikesum = spikesum.loc[spikesum["spike"]>1]
    
#    if j =="Net_Job_Creation":
#        print(p75_abs_year2year)
#        print(subset)
#    if j=="Firms":
    #!cvarref
    for q,z in list(zip(spikesum[cvar1],spikesum[cvar2])):
        #print(str(q)+str(z))
        x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z), "year2"]
        y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z), j]
        x2 =subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["spike"]==1), "year2"]
        v = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["spike"]==1), j]
        plt.plot(x, y)
        plt.plot(x2,v,'ro')
        filestring = "../output/plot_"+str(a)+str(j)+"_"+str(q)+str(z).replace(")","")+".png"
        filestring = filestring.replace(" ","_")
        plt.savefig(filestring)
        plt.clf()


def spikefunction1(subset,var,a,j,cvar2=""):
    pd.options.mode.chained_assignment = 'raise'        
    subset =subset.assign(ntm1=subset[var].shift(1))        
    subset.loc[:,"ntp1"] = subset[var].shift(-1)        
    subset.loc[:,"ntp2"] = subset[var].shift(-2)        
    subset.loc[:,"year2year"] = subset[var]-subset["ntm1"]        
    subset.loc[:,"year2yearm1"] =subset["year2year"] .shift(1)        
    subset.loc[:,"year2yearp1"] =subset["year2year"] .shift(-1)        
    subset.loc[:,"year2yearp2"] =subset["year2year"] .shift(-2)        
    subset.loc[:,"abs_year2year"] = abs(subset["year2year"])        
    subset.loc[:,"abs_year2yearp1"] = subset["abs_year2year"].shift(-1)        
    subset.loc[:,"abs_year2yearm1"] = subset["abs_year2year"].shift(1)        
    subset.loc[:,"abs_year2yearp2"] = subset["abs_year2year"].shift(-2)              
    subset.loc[:,"sc"] = 0
    subset.loc[:,"sf"] = 0        
    
    f = {'abs_year2year': [q3]}
    q75=subset[["abs_year2year",cvar2]].groupby([cvar2]).agg(f).reset_index()
    #!cvarref
    q75.columns = [cvar2,"q3"]
    #!cvarref
    subset=subset.merge(q75, on=[cvar2])  
#    p75_abs_year2year = subset["abs_year2year"].quantile([.75]).item()  
            
    #outlier parameters        
    subset.loc[:,"op"] = 0        
    subset.loc[subset["abs_year2year"] > p1*subset["q3"], "op"] +=1        
    subset.loc[(subset["ntm1"] !=0) & (subset["abs_year2year"]/subset["ntm1"] > p2), "op"] += 1        
    subset.loc[subset["ntm1"] == 0, "op"] += 1        
    subset.loc[subset["abs_year2year"] > p3, "op"] += 1        
    subset.loc[subset["year2year"]>=0, "sc"] = 1        
    subset.loc[subset["year2yearp1"]>=0, "sf"] = 1        
    subset.loc[(subset["sc"] != subset["sf"]) & (subset["abs_year2yearp1"] >= subset["abs_year2year"]*p4), "op" ] += 1                      
    
    #special rules for first and last
    subset.loc[:,"Last"] = 0      
    #!cvarref    
    last_row_index = subset.groupby([cvar2]).tail(1).index.values             
    subset.loc[last_row_index, "Last"] = 1        
    subset.loc[last_row_index, "op"] = 0  
    subset.loc[last_row_index, "sc"] = 0        
    subset.loc[last_row_index, "sf"] = 0
                              
    subset.loc[:,"First"] = 0   
    #!cvarref
    first_row_index = subset.groupby([cvar2]).head(1).index.values             
    subset.loc[first_row_index, "First"] = 1        
    subset.loc[first_row_index, "op"] = 0
    subset.loc[first_row_index, "sc"] = 0        
    subset.loc[first_row_index, "sf"] = 0
        
    #first adjustments
    subset.loc[(subset["abs_year2yearp1"] > p1*subset["q3"]) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset[var] !=0) & (subset["abs_year2yearp1"]/subset[var] > p2) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset[var] ==0) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset["abs_year2yearp1"] > p3) & (subset["First"] == 1), "op"] += 1        
    subset.loc[(subset["year2yearp1"]>=0) & (subset["First"] == 1), "sc"] = 1        
    subset.loc[(subset["year2yearp2"]>=0) & (subset["First"] == 1), "sf"] = 1        
    subset.loc[(subset["sc"] == subset["sf"]) & (subset["First"] == 1), "op" ] += 1        
    subset.loc[(subset["sc"] != subset["sf"]) & (subset["First"] != 1) & (subset["abs_year2yearp2"] < subset["abs_year2yearp1"]*p4) & (subset["First"] == 1), "op" ] += 1
    
    #last adjustments
    subset.loc[(subset["abs_year2year"] > p1*subset["q3"]) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["ntm1"] !=0) & (subset["abs_year2year"]/subset["ntm1"] > p2) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["ntm1"] ==0) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["abs_year2year"] > p3) & (subset["Last"] == 1), "op"] += 1        
    subset.loc[(subset["year2year"]>=0) & (subset["Last"] == 1), "sc"] = 1        
    subset.loc[(subset["year2yearm1"]>=0) & (subset["Last"] == 1), "sf"] = 1        
    subset.loc[(subset["sc"] == subset["sf"]) & (subset["Last"] == 1), "op" ] += 1        
    subset.loc[(subset["sc"] != subset["sf"]) & (subset["Last"] != 1) & (subset["abs_year2yearm1"] < subset["abs_year2year"]*p4) & (subset["Last"] == 1), "op" ] += 1
    
    #special rules
    #!cvarref
    if cvar2 == "fage4":
        subset.loc[(subset[cvar2]=="g) 6 to 10") & (subset["year2"]<=1987), "op"]=-1
        subset.loc[(subset[cvar2]=="h) 11 to 15") & (subset["year2"]<=1992), "op"]=-1
        subset.loc[(subset[cvar2]=="i) 16 to 20") & (subset["year2"]<=1997), "op"]=-1 
        subset.loc[(subset[cvar2]=="j) 21 to 25") & (subset["year2"]<=2002), "op"]=-1                
    
    #check for outliers
    subset.loc[:,"spike"]=0
    subset.loc[subset["op"]>3, "spike"]=1
    #!cvarref
    spikesum = subset[[cvar2,"spike"]].groupby([cvar2]).sum().reset_index()
    spikesum = spikesum.loc[spikesum["spike"]>1]
    
#    if j =="Net_Job_Creation":
#        print(p75_abs_year2year)
#        print(subset)
#    if j=="Firms":
    #!cvarref
    for z in list(spikesum[cvar2]):
        #print(str(q)+str(z))
        x = subset.loc[(subset[cvar2]==z), "year2"]
        y = subset.loc[(subset[cvar2]==z), j]
        x2 =subset.loc[(subset[cvar2]==z) & (subset["spike"]==1), "year2"]
        v = subset.loc[(subset[cvar2]==z) & (subset["spike"]==1), j]
        plt.plot(x, y)
        plt.plot(x2,v,'ro')
        filestring = "../output/plot_"+str(a)+str(j)+"_"+str(z).replace(")","")+".png"
        filestring = filestring.replace(" ","_")
        plt.savefig(filestring)
        plt.clf()

for z in files:   
    dfile = z 
    data = pd.read_csv(ddirectory+dfile)
    fvariable=[]
    fvariable1=["Firms","Estabs","Emp","Denom","Estabs_Entry","Estabs_Exit","Job_Creation","Job_Creation_Births","Job_Creation_Continuers","Job_Destruction","Job_Destruction_Deaths","Job_Destruction_Continuers","Net_Job_Creation","Firmdeath_Firms","Firmdeath_Estabs","Firmdeath_Emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]
    fvariable2=["firms","estabs","emp","denom","estabs_entry","estabs_exit","job_creation","job_creation_births","job_creation_continuers","job_destruction","job_destruction_deaths","job_destruction_continuers","net_job_creation","firmdeath_firms","firmdeath_estabs","firmdeath_emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]
    for i,j in zip(fvariable1,fvariable2):
        if i in list(data):
            fvariable.append(i)
        if j in list(data):
            fvariable.append(j)
    if "Denom" in list(data):
        data.loc[:,"alt_emp"]=data["Denom"] + .5*(data["Job_Creation"] - data["Job_Destruction"])
        cap=1
    else:
        data.loc[:,"alt_emp"]=data["denom"] + .5*(data["job_creation"] - data["job_destruction"])
        cap=0
    lvariable=list(data)
    if "Firms" in list(data):
        ci=data.columns.get_loc('Firms')
    else:
        ci=data.columns.get_loc('firms')

                #run analysis on subset data        
                #calculations
#no variable tables
    if ci ==1:
        subset=data
        var=j
        #spikefunction(subset,var,z)
#one variable tables
    if ci==2:
        cvar=lvariable[1]
        for j in fvariable:
            var = j
            vlist=data[j].unique()
            clist=data[cvar].unique()
            data.sort_values([cvar,"year2"], inplace=True)            
            spikefunction1(data,var,z,j,cvar)
           

#two variable tables
    if ci==3:
        cvar=lvariable[1]
        cvar2=lvariable[2]   
        #subset values
        for j in fvariable:
            var = j
            vlist=data[j].unique()
            clist=data[cvar].unique()
            clist2=data[cvar2].unique()
            data.sort_values([cvar,cvar2,"year2"], inplace=True)
            #data = data.loc[(data[cvar] == 33460) & (data[cvar2] == "j) 2500 to 4999")]
            #print(data.head(10))            
            #spikefunction2(data,var,z,j,cvar,cvar2)

print("--- %s seconds ---" % (time.time() - start_time))