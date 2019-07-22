# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:56:06 2019

@author: beggs005
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import argparse
import tkinter as tk
import numpy as np
import sys

start_time= time.time()

   
time1= time.time()


class qaGUI:
    def __init__(self,window):
        self.window = window
        self.len_max=0
        self.labelt = tk.Label(window, text="Select Tables:", anchor="w", font="Arial 12 bold")
#        self.e = tk.Entry(window)
#        self.labele = tk.Label(window, text="Table Name:", anchor="w", font="Arial 12")
        self.s = tk.Scrollbar(window)
        self.labelt.grid(row=0,column=0)
#        self.labele.grid(row=1,column=0)
#       self.e.grid(row=1,column=0, sticky='w')
        self.s.grid(row=2,column=1,sticky='ns')
        vtable=['All']+table_dict_values
        
        qaGUI.p1 = args.parameter1
        qaGUI.p2 = args.parameter2

        
        qaGUI.od = args.outdirectory
        
        self.list_box = tk.Listbox(window, selectmode="multiple", listvariable=vtable)
        for i,j in zip(range(len(vtable)),vtable):
            if len(j) > self.len_max:
                self.len_max= len(j)
            self.list_box.insert(i, str(j))
        self.list_box.grid(row=2,column=0,sticky='ns')
        self.s['command'] = self.list_box.yview
        self.list_box['yscrollcommand'] = self.s.set
        self.list_box.config(width=self.len_max)


        def var_window():
            window.withdraw()
            qaGUI.entered_table = self.e.get()
            ndex = self.list_box.curselection()
            qaGUI.selected_tables=[self.list_box.get(x) for x in ndex]
            var_win = tk.Toplevel()
            labelv = tk.Label(var_win, text="Select Variables:", anchor="w",font="Arial 12 bold")
            labelv.grid(row=0,column=0)
            sv = tk.Scrollbar(var_win)
            sv.grid(row=1,column=1,sticky='ns')
            vvar=['All'] + fvariable1
            list_boxv = tk.Listbox(var_win, selectmode="multiple", listvariable=vvar)
            for i,j in zip(range(len(vvar)),vvar):
                list_boxv.insert(i, str(j))
            list_boxv.grid(row=1,column=0,sticky='ns')
            sv['command'] = list_boxv.yview
            list_boxv['yscrollcommand'] = sv.set
            list_boxv.config(width="0")
            framev = tk.Frame(var_win)
            framev.grid(row=2,column=0)
            def close_var():
                ndexv = list_boxv.curselection()
                qaGUI.selected_variables=[list_boxv.get(x) for x in ndexv]
                var_win.withdraw()
                open_ltb()

            def open_ltb():
                list_params = tk.Toplevel()
                selected_tables= qaGUI.selected_tables
                entered_table= qaGUI.entered_table
                selected_variables= qaGUI.selected_variables

                if selected_tables == []:
                    if entered_table == "":
                        selected_tables = "All"
                
                if entered_table != "":
                    selected_tables = entered_table.replace(" ","").split(",") + selected_tables
                
                if 'All' in selected_tables:
                    selected_tables = "All"
                    
                if selected_variables == []:
                    selected_variables = "All"
                
                if 'All' in selected_variables:
                    selected_variables = "All"

                v1 = tk.StringVar()
                v2 = tk.StringVar()
                vod = tk.StringVar() 
              
               
                labelall = tk.Label(list_params, text="Current Selections:", anchor="w",font="Arial 12 bold")
                labeltables = tk.Label(list_params, text="Selected Tables:", anchor="w",font="Arial 10")
                labelvar = tk.Label(list_params, text="Selected Variables:", anchor="w",font="Arial 10")
                labelp1 = tk.Label(list_params, text="P1:", anchor="w",font="Arial 10")
                labelp2 = tk.Label(list_params, text="P2:", anchor="w",font="Arial 10")
                labelod = tk.Label(list_params, text="Out Directory:", anchor="w",font="Arial 10")
                
                labeltablesa = tk.Label(list_params, text=str(selected_tables).strip("[").strip("]").replace("'",""), anchor="w",font="Arial 10", wraplength=300)
                labelvara = tk.Label(list_params, text=str(selected_variables).strip("[").strip("]").replace("'",""), anchor="w",font="Arial 10", wraplength=300)
                labelp1a = tk.Label(list_params, textvariable=v1, anchor="w",font="Arial 10")
                labelp2a = tk.Label(list_params, textvariable=v2, anchor="w",font="Arial 10")
                labeloda = tk.Label(list_params, textvariable=vod, anchor="w",font="Arial 10")
                
                v1.set(qaGUI.p1)
                v2.set(qaGUI.p2)
                vod.set(qaGUI.od)
                
                labelall.grid(row=1,column=0)
                labeltables.grid(row=2,column=0)
                labelvar.grid(row=3,column=0)
                labelp1.grid(row=4,column=0)
                labelp2.grid(row=5,column=0)
                labelod.grid(row=8,column=0)                 

                labeltablesa.grid(row=2,column=1)
                labelvara.grid(row=3,column=1)
                labelp1a.grid(row=4,column=1)
                labelp2a.grid(row=5,column=1)
                labeloda.grid(row=8,column=1)                  
                
                def var_params():
                    list_params.withdraw()
                    var_par = tk.Toplevel()
                    labelv = tk.Label(var_par, text="Enter Parameters:", anchor="w",font="Arial 12 bold")
                    labelv.grid(row=0,column=0, columnspan=2)
                    lp1 = tk.Label(var_par, text="Parameter 1:", anchor="w",font="Arial 10")
                    lp1.grid(row=1,column=0)
                    lp2 = tk.Label(var_par, text="Parameter 2:", anchor="w",font="Arial 10")
                    lp2.grid(row=2,column=0)
                    lod = tk.Label(var_par, text="Out Directory:", anchor="w",font="Arial 10")
                    lod.grid(row=5,column=0)
                    ep1 = tk.Entry(var_par)
                    ep1.grid(row=1,column=1, sticky='w')
                    ep2 = tk.Entry(var_par)
                    ep2.grid(row=2,column=1, sticky='w')
                    eod = tk.Entry(var_par)
                    eod.grid(row=5,column=1, sticky='w')
        #            framep = tk.Frame(var_par)
        #            framep.grid(row=5,column=0, columnspan=2)
                    def close_par():
                        if ep1.get() !="":
                            qaGUI.p1=ep1.get()
                        if ep2.get() !="":
                            qaGUI.p2=ep2.get()
                        if eod.get() !="":
                            qaGUI.od=eod.get()
                        var_par.withdraw()
                        v1.set(qaGUI.p1)
                        v2.set(qaGUI.p2)
                        vod.set(qaGUI.od)
                        list_params.deiconify()
                    buttonv = tk.Button(var_par, text = "Submit", command = close_par)
                    buttonv.grid(row=6,column=0, columnspan=2)
                def close_all():
                    window.destroy()
                def restart():
                    python = sys.executable
                    os.execl(python, python, * sys.argv)
                button1 = tk.Button(list_params, text = "Edit Parameters", command = var_params)
                button1.grid(row=9,column=0, columnspan=1)
                buttona = tk.Button(list_params, text = "Submit", command = close_all)
                buttona.grid(row=10,column=0, columnspan=2)
                buttonr = tk.Button(list_params, text = "Restart", command = restart)
                buttonr.grid(row=9,column=1, columnspan=1)

                
                
            buttonv = tk.Button(framev, text = "Next", command = close_var)
            buttonv.grid(row=9,column=0)

			
        
    
        self.frame = tk.Frame(window)
        self.frame.grid(row=3,column=0)
        self.e = tk.Entry(window, width=self.len_max)
        self.e.grid(row=1,column=0, sticky='w')
#        self.button1 = tk.Button(self.frame, text = "Edit Parameters", command = var_params)
#        self.button1.grid(row=4,column=0)
        self.button = tk.Button(self.frame, text = "Next", command = var_window)
        self.button.grid(row=5,column=0)
        
class qaMain:
        def __init__(self,ddirectory,vdirectory,selected_tables,selected_variables, vintage_tables):
            self.ddirectory=ddirectory
            self.vdirectory=vdirectory
            self.selected_tables=selected_tables
            self.vintage_tables = vintage_tables
            self.selected_variables = selected_variables
            self.selected_variables1 = [item.lower() for item in selected_variables]
            self.catlist1=["fage4","ifsize","metro","fsize","state","sic1","msa","Fage4","Ifsize","Metro","Fsize","State","Sic1","Msa","age4","Age4","size","Size","isize","Isize"]        
            for z in self.selected_tables:   
                dfile = z 
                data = pd.read_csv(self.ddirectory+dfile+".csv") 
                data['max_year']=max(data['year2'])
                fvariable=[]
            #    data.dropna(axis=1,how='all')
            #    print(data['sic1'].isnull().all())
                if "Denom" in list(data):
                    data.loc[:,"alt_emp"]=data["Denom"] + .5*(data["Job_Creation"] - data["Job_Destruction"])
                elif "denom" in list(data):
                    data.loc[:,"alt_emp"]=data["denom"] + .5*(data["job_creation"] - data["job_destruction"])
                for i,j in zip(self.selected_variables,self.selected_variables1):
                    if i in list(data):
                        fvariable.append(i)
                    if j in list(data):
                        fvariable.append(j)
            for z in self.vintage_tables:   
                dfile = z 
                datav = pd.read_csv(self.vdirectory+dfile)
                datav['max_year']=max(datav['year2'])
#                fvariable=[]
            #    data.dropna(axis=1,how='all')
            #    print(data['sic1'].isnull().all())
                if "Denom" in list(data):
                    data.loc[:,"alt_emp"]=data["Denom"] + .5*(data["Job_Creation"] - data["Job_Destruction"])
                elif "denom" in list(data):
                    data.loc[:,"alt_emp"]=data["denom"] + .5*(data["job_creation"] - data["job_destruction"])
#                for i,j in zip(self.selected_variables,self.selected_variables1):
#                    if i in list(data):
#                        fvariable.append(i)
#                    if j in list(data):
#                        fvariable.append(j)
#            
            cilist=list(set(list(data)) & set(self.catlist1))
            def removelist(datax,x):
                return [value for value in x if datax[value].isnull().all() == False]
            cilist= removelist(data, cilist)
            ci = len(cilist)
            print(z)
            print(ci)
                            #run analysis on subset data        
                            #calculations
        #no variable tables
            if ci ==0:
                data = data.merge(datav, on = "year2", suffixes=("","_vint"))
                data.sort_values("year2", inplace=True) 
                for j in fvariable:
                    
                    qaMain.vintagefunction(data,z,j)
        #one variable tables
            if ci==1:
                cvar=cilist[0]
                data = data.merge(datav, on = ["year2",cvar], suffixes=("","_vint"))
                data.sort_values([cvar,"year2"], inplace=True) 
                for j in fvariable:
                    
                               
                    qaMain.vintagefunction(data,z,j,cvar)
        
        #two variable tables
            if ci==2:
                cvar=cilist[0]
                cvar2=cilist[1]
                data = data.merge(datav, on = ["year2",cvar, cvar2], suffixes=("","_vint"))
                data.sort_values([cvar,cvar2,"year2"], inplace=True)
                #subset values
                for j in fvariable:
                    
                             
                    qaMain.vintagefunction(data,z,j,cvar,cvar2)
        #three variable tables
            if ci==3:
                cvar=cilist[0]
                cvar2=cilist[1]
                cvar3=cilist[2]
                data = data.merge(datav, on = ["year2",cvar, cvar2, cvar3], suffixes=("","_vint"))
                data.sort_values([cvar,cvar2,cvar3,"year2"], inplace=True) 
                #subset values
                for j in fvariable:
                             
                    qaMain.vintagefunction(data,z,j,cvar,cvar2,cvar3)
        
        #four variable tables
            if ci==4:
                cvar=cilist[0]
                cvar2=cilist[1]
                cvar3=cilist[2]
                cvar4=cilist[3]
                data = data.merge(datav, on = ["year2",cvar, cvar2, cvar3, cvar4], suffixes=("","_vint"))
                data.sort_values([cvar,cvar2,cvar3,cvar4,"year2"], inplace=True) 
                #subset values
                for j in fvariable:
                    qaMain.vintagefunction(data,z,j,cvar,cvar2,cvar3,cvar4)
        def vintagefunction(subset,a,j,cvar1="",cvar2="",cvar3="",cvar4=""):
            var = j
            var_vint = j+"_vint"
            subset["abs_vint2vint"]=abs(subset[var_vint].astype(float)-subset[var].astype(float))
            try: 
                subset["%_abs_vint2vint"]= (subset[var_vint].astype(float)-subset[var].astype(float))/subset[var_vint].astype(float)
            except:
                subset["%_abs_vint2vint"]=0
            subset["vintage_o"] = 0
            subset.loc[(subset["abs_vint2vint"] > p1) & (subset["%_abs_vint2vint"] > p2), "vintage_o"]=1
            subset.loc[(subset["abs_vint2vint"] > p1) & (subset[var_vint].astype(float) == 0), "vintage_o"]=1
            
            spikesum1 = subset["vintage_o"].sum() 
            
            if cvar1 == "":
                spikesum1 = subset["vintage_o"].sum() 
            
            if (cvar1 != "") & (cvar2 == ""):
                spikesum = subset[[cvar1,"vintage_o"]].groupby([cvar1]).sum().reset_index()
                spikesum = spikesum.loc[spikesum["vintage_o"]>1]
        
            if (cvar2 != "") & (cvar3 == ""):
                spikesum = subset[[cvar1,cvar2,"vintage_o"]].groupby([cvar1,cvar2]).sum().reset_index()
                spikesum = spikesum.loc[spikesum["vintage_o"]>1]
                
            if (cvar3 != "") & (cvar4 == ""):
                spikesum = subset[[cvar1,cvar2,cvar3,"vintage_o"]].groupby([cvar1,cvar2,cvar3]).sum().reset_index()
                spikesum = spikesum.loc[spikesum["vintage_o"]>1]
                
            if cvar4 != "":
                spikesum = subset[[cvar1,cvar2,cvar3,cvar4,"vintage_o"]].groupby([cvar1,cvar2,cvar3,cvar4]).sum().reset_index()
                spikesum = spikesum.loc[spikesum["vintage_o"]>1]   
                
            def plot_maker(a,j,cvar1,cvar2,cvar3,cvar4,x,y,x2,y2,k,kv,kc,plttitle,filestring):
                plt.scatter(x, y, s=20)
                plt.plot(x2,y2,'ro', markersize=10)
                for i, txt in zip(k.index,k):#enumerate(k):
                    plt.annotate(txt, (x2[i],y2[i]), size=9)
                x3=np.linspace(min(x),max(x))
                plt.plot(x3,x3)
                plt.title(plttitle,loc='center')
                plt.ylabel(str(j)+"_"+str(kc))
                plt.xlabel(str(j)+"_"+str(kv))
                plt.tight_layout()
                print("Outlier found in "+str(a).replace(".csv","")+". Writing "+str(filestring))
                plt.savefig(filestring)
                plt.clf()
                
            if (cvar1 == "") & (spikesum1>0) & (cvar2 ==""):
                x = subset[var_vint]
                y = subset[var]
                x2=subset.loc[(subset["vintage_o"]==1)][var_vint]
                y2=subset.loc[(subset["vintage_o"]==1)][var]
                k=subset.loc[(subset["vintage_o"]==1)]["year2"]
                kv=max(subset['max_year_vint'])
                kc=max(subset['max_year'])
                plttitle = str(a).replace(".csv","")+"""
"""+str(j)
                filestring = odirectory+str(a).replace(".csv","")+"."+str(j)+".png"
                filestring = filestring.replace(" ","_").replace(")","")
                if subset["vintage_o"].sum() > 0:
                    plot_maker(a,j,cvar1,cvar2,cvar3,cvar4,x,y,x2,y2,k,kv,kc,plttitle)
            
            if (cvar1 != "") & (cvar2 == ""):
                for z in list(spikesum[cvar1]):
                    x = subset.loc[(subset[cvar1]==z),var_vint]
                    y = subset.loc[(subset[cvar1]==z),var]
                    x2=subset.loc[(subset[cvar1]==z) & (subset["vintage_o"]==1)][var_vint]
                    y2=subset.loc[(subset[cvar1]==z) & (subset["vintage_o"]==1)][var]
                    k=subset.loc[(subset[cvar1]==z) & (subset["vintage_o"]==1)]["year2"]
                    kv=max(subset['max_year_vint'])
                    kc=max(subset['max_year'])
                    plttitle = str(a).replace(".csv","")+"""
"""+cvar1+": "+str(z)+"""
"""+str(j)
                    filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(z)+"."+str(j)+".png"
                    filestring = filestring.replace(" ","_").replace(")","")
                    if subset["vintage_o"].sum() > 0:
                        plot_maker(a,j,cvar1,cvar2,cvar3,cvar4,x,y,x2,y2,k,kv,kc,plttitle,filestring)
                    
            if (cvar2 != "") & (cvar3 == ""):
                for q,z in list(zip(spikesum[cvar1],spikesum[cvar2])):
                    #print(str(q)+str(z))                    
                    x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z),var_vint]
                    y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z),var]
                    x2=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["vintage_o"]==1)][var_vint]
                    y2=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["vintage_o"]==1)][var]
                    k=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["vintage_o"]==1)]["year2"]
                    kv=max(subset['max_year_vint'])
                    kc=max(subset['max_year'])
                    plttitle = str(a).replace(".csv","")+"""
"""+cvar1+": "+str(q)+"""
"""+cvar2+": "+str(z)+"""
"""+str(j)
                    filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(q)+"."+cvar2+"_"+str(z)+"."+str(j)+".png"
                    filestring = filestring.replace(" ","_").replace(")","")
                    if subset["vintage_o"].sum() > 0:
                        plot_maker(a,j,cvar1,cvar2,cvar3,cvar4,x,y,x2,y2,k,kv,kc,plttitle,filestring)
                    
            if (cvar3 != "") & (cvar4 == ""):
                for q,z,o in list(zip(spikesum[cvar1],spikesum[cvar2],spikesum[cvar3])):
                    
                    x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o),var_vint]
                    y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o),var]
                    x2=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset["vintage_o"]==1)][var_vint]
                    y2=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset["vintage_o"]==1)][var]
                    k=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset["vintage_o"]==1)]["year2"]
                    kv=max(subset['max_year_vint'])
                    kc=max(subset['max_year'])
                    plttitle = str(a).replace(".csv","")+"""
"""+cvar1+": "+str(q)+"""
"""+cvar2+": "+str(z)+"""
"""+cvar3+": "+str(o)+"""
"""+str(j)
                    filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(q)+"."+cvar2+"_"+str(z)+"."+cvar3+"_"+str(o)+"."+str(j)+".png"
                    filestring = filestring.replace(" ","_").replace(")","")
                    if subset["vintage_o"].sum() > 0:
                        plot_maker(a,j,cvar1,cvar2,cvar3,cvar4,x,y,x2,y2,k,kv,kc,plttitle,filestring)
                    

            if cvar4 != "":
                for q,z,o,p in list(zip(spikesum[cvar1],spikesum[cvar2],spikesum[cvar3],spikesum[cvar4])):
                    
                    x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p),var_vint]
                    y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p),var]
                    x2=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p) & (subset["vintage_o"]==1)][var_vint]
                    y2=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p) & (subset["vintage_o"]==1)][var]
                    k=subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p) & (subset["vintage_o"]==1)]["year2"]
                    kv=max(subset['max_year_vint'])
                    kc=max(subset['max_year'])
                    plttitle = str(a).replace(".csv","")+"""
"""+cvar1+": "+str(q)+"""
"""+cvar2+": "+str(z)+"""
"""+cvar3+": "+str(o)+"""
"""+cvar4+": "+str(p)+"""
"""+str(j)
                    filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(q)+"."+cvar2+"_"+str(z)+"."+str(j)+".png"
                    filestring = filestring.replace(" ","_").replace(")","")
                    if subset["vintage_o"].sum() > 0:
                        plot_maker(a,j,cvar1,cvar2,cvar3,cvar4,x,y,x2,y2,k,kv,kc,plttitle,filestring)



if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
#    parser.add_argument('--table','-t', help="Table input use 'all' for all tables in directory",type = str, default = 'all')
    parser.add_argument('--parameter1', '-p1', help="First Parameter defined in Section E", type = float, default = 500)
    parser.add_argument('--parameter2', '-p2', help="Second Parameter defined in Section E", type = float, default = .1)
#    parser.add_argument('--varn', '-vn', help="Variable to run through QA", type = str, default = 'all')
    
    parser.add_argument('--datadirectory', '-dd', help="Directory where data is stored end with /", type = str, default = '/lbd/bitsi/ewdwork/datatables/')
    parser.add_argument('--lookupdirectory', '-ld', help="Directory where lookup lists are stored end with /", type = str, default = '/lbd/bitsi/ewdwork/data/')
    parser.add_argument('--outdirectory', '-od', help="Directory where output files are written, end with /", type = str, default = '/lbd/bitsi/ewdwork/output/')
    parser.add_argument('--vintdirectory', '-vd', help="Directory where vintage data is stored end with /", type = str, default = '/lbd/bitsi/ewdwork/datatables2013/')
    parser.add_argument('--testing', '-t', help="Indicates if being run with testing set, 1 for testing", type = int, default = 0)
    args = parser.parse_args()

    #read in data table
    ddirectory = args.datadirectory
    ldirectory = args.lookupdirectory
    odirectory= args.outdirectory
    vdirectory= args.vintdirectory
    
    
    table_dict = {	'bds_f_all_release.csv': ['bds_f_all_release', 1]		,
	'bds_e_all_release.csv': ['bds_e_all_release', 2]		,
	'bds_f_sic_release.csv': ['bds_f_sic_release', 3]		,
	'bds_e_sic_release.csv': ['bds_e_sic_release', 4]		,
	'bds_f_sz_release.csv': ['bds_f_sz_release', 5]		,
	'bds_e_sz_release.csv': ['bds_e_sz_release', 6]		,
	'bds_f_isz_release.csv': ['bds_f_isz_release', 7]		,
	'bds_e_isz_release.csv': ['bds_e_isz_release', 8]		,
	'bds_f_age_release.csv': ['bds_f_age_release', 9]		,
	'bds_e_age_release.csv': ['bds_e_age_release', 10]		,
	'bds_f_st_release.csv': ['bds_f_st_release', 11]		,
	'bds_e_st_release.csv': ['bds_e_st_release', 12]		,
	'bds_f_metrononmetro_release.csv': ['bds_f_metrononmetro_release', 13]		,
	'bds_f_msa_release.csv': ['bds_f_msa_release', 14]		,
	'bds_e_msa_release.csv': ['bds_e_msa_release', 15]		,
	'bds_f_agesz_release.csv': ['bds_f_agesz_release', 16]		,
	'bds_e_agesz_release.csv': ['bds_e_agesz_release', 17]		,
	'bds_f_ageisz_release.csv': ['bds_f_ageisz_release', 18]		,
	'bds_e_ageisz_release.csv': ['bds_e_ageisz_release', 19]		,
	'bds_f_agesic_release.csv': ['bds_f_agesic_release', 20]		,
	'bds_e_agesic_release.csv': ['bds_e_agesic_release', 21]		,
	'bds_f_agemetrononmetro_release.csv': ['bds_f_agemetrononmetro_release', 22]		,
	'bds_f_agemsa_release.csv': ['bds_f_agemsa_release', 23]		,
	'bds_f_agest_release.csv': ['bds_f_agest_release', 24]		,
	'bds_e_agest_release.csv': ['bds_e_agest_release', 25]		,
	'bds_f_szsic_release.csv': ['bds_f_szsic_release', 26]		,
	'bds_e_szsic_release.csv': ['bds_e_szsic_release', 27]		,
	'bds_f_szmetrononmetro_release.csv': ['bds_f_szmetrononmetro_release', 28]		,
	'bds_f_szmsa_release.csv': ['bds_f_szmsa_release', 29]		,
	'bds_f_szst_release.csv': ['bds_f_szst_release', 30]		,
	'bds_e_szst_release.csv': ['bds_e_szst_release', 31]		,
	'bds_f_iszsic_release.csv': ['bds_f_iszsic_release', 32]		,
	'bds_e_iszsic_release.csv': ['bds_e_iszsic_release', 33]		,
	'bds_f_iszmetrononmetro_release.csv': ['bds_f_iszmetrononmetro_release', 34]		,
	'bds_f_iszst_release.csv': ['bds_f_iszst_release', 35]		,
	'bds_e_iszst_release.csv': ['bds_e_iszst_release', 36]		,
	'bds_f_agesz_sic_release.csv': ['bds_f_agesz_sic_release', 37]		,
	'bds_e_agesz_sic_release.csv': ['bds_e_agesz_sic_release', 38]		,
	'bds_f_agesz_st_release.csv': ['bds_f_agesz_st_release', 39]		,
	'bds_e_agesz_st_release.csv': ['bds_e_agesz_st_release', 40]		,
	'bds_f_ageszmetrononmetro_release.csv': ['bds_f_ageszmetrononmetro_release', 41]		,
	'bds_f_agesz_msa_release.csv': ['bds_f_agesz_msa_release', 42]		,
	'bds_f_ageisz_sic_release.csv': ['bds_f_ageisz_sic_release', 43]		,
	'bds_e_ageisz_sic_release.csv': ['bds_e_ageisz_sic_release', 44]		,
	'bds_f_ageisz_st_release.csv': ['bds_f_ageisz_st_release', 45]		,
	'bds_e_ageisz_st_release.csv': ['bds_e_ageisz_st_release', 46]		,
	'bds_f_ageiszmetro_release.csv': ['bds_f_ageiszmetro_release', 47]		,
	'bds_f_ageszmetro_state_release.csv': ['bds_f_ageszmetro_state_release', 48]		,
	'bds_f_ageiszmetro_state_release.csv': ['bds_f_ageiszmetro_state_release', 49]		}    
    
    files = [f for f in os.listdir(ddirectory) if os.path.isfile(os.path.join(ddirectory,f))]
    filesv = [f for f in os.listdir(vdirectory) if os.path.isfile(os.path.join(vdirectory,f))]
    fvariable1=["Firms","Estabs","Emp","Denom","Estabs_Entry","Estabs_Exit","Job_Creation","Job_Creation_Births","Job_Creation_Continuers","Job_Destruction","Job_Destruction_Deaths","Job_Destruction_Continuers","Net_Job_Creation","Firmdeath_Firms","Firmdeath_Estabs","Firmdeath_Emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]
    fvariable2=["firms","estabs","emp","denom","estabs_entry","estabs_exit","job_creation","job_creation_births","job_creation_continuers","job_destruction","job_destruction_deaths","job_destruction_continuers","net_job_creation","firmdeath_firms","firmdeath_estabs","firmdeath_emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]

        
    for f in list(table_dict.keys()):
        if f not in files:
            del table_dict[f]    
    for f in files:
        if f not in list(table_dict.keys()):
            table_dict.update({f:[f.replace(".csv",""),len(table_dict)+1]})

            
    table_dict_values = [table_dict[i][0] for i in table_dict.keys()]  
        
    
    p1 = args.parameter1
    p2 = args.parameter2
    
    master = tk.Tk()
    window = qaGUI(master)
	
    tk.mainloop()
    try: window.p1
    except AttributeError: window.p1 = None
    if window.p1 != None:
        if float(window.p1) !="":
            p1 = float(window.p1)
    try: window.p2
    except AttributeError: window.p2 = None
    if window.p2 != None:
        if float(window.p2) !="":
            p2 = float(window.p2)
    try: window.od
    except AttributeError: window.od = None
    if window.od != None:
        if str(window.od) !="":
           odirectory  = str(window.od)
    
    if not odirectory.endswith("/"):
        odirectory= odirectory + "/"
    
    selected_tables= window.selected_tables
    entered_table= window.entered_table
    selected_variables= window.selected_variables


	
    time2= time.time()
    if selected_tables == []:
        if entered_table == "":
            selected_tables = table_dict_values
        else:
            assert set(entered_table.replace(" ","").split(",")).issubset(table_dict_values), "Entered Table Not Found in Directory"
            selected_tables = entered_table.replace(" ","").split(",")
    
    if entered_table != "":
        selected_tables = entered_table.replace(" ","").split(",") + selected_tables
    
    if 'All' in selected_tables:
        selected_tables = table_dict_values
        
    if selected_variables == []:
        selected_variables = fvariable1
    
    if 'All' in selected_variables:
        selected_variables = fvariable1
    
    time2= time.time()
    
    
    def change_name_func(x):
        vdlist =[]
        for j in x:
            #change name function if needed:
            print(j)
            h=j+".csv"
            warningstr = "Vintage file" +str(h)+ "not found"
            assert h in filesv, warningstr
            vdlist.append(h)
        return vdlist
    
    vintage_tables=change_name_func(selected_tables)
            
            

    print("Tables Selected:")
    print(selected_tables)
    print("Variables Selected:")
    print(selected_variables)

    qaMain(ddirectory,vdirectory,selected_tables,selected_variables,vintage_tables)    
    

    
        
    
totaltime=time.time() - start_time
skiptime=time2-time1

print("--- %s seconds ---" % (totaltime-skiptime))