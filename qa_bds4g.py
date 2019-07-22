# -*- coding: utf-8 -*-

"""
Created on Thu Apr 11 12:47:26 2019
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
import datetime as dt

start_time= time.time()

datadirectorystr = '/lbd/bitsi/ewdwork/datatables/'
lookupdirectorystr =  '/lbd/bitsi/ewdwork/data/'
outdirectorystr= '/lbd/bitsi/ewdwork/output/'



time1= time.time()

#class ResizingCanvas(Canvas):
#    def __init__(self,parent,**kwargs):
#        Canvas.__init__(self,parent,**kwargs)
#        self.bind("<configue>", self.on_resize)
#        self.height= self.winfo_reqheight()
#        self.width= self.hinfo_reqwidth()
#    def on_resize(self, event):
#        wscale = float(event.width)/self.width
#        hscale = float(event.height)/self.height
#        self.width = event.width
#        self.hiehgt = event.height
#        self.config(width=self.width, height=self.height)
#        self.scale("all",0,0,wscale,hscale)
        
class qaGUI:
    def __init__(self,window):
        self.window=window
        self.len_max=0
        window.grid_columnconfigure(0,weight=1)
        window.grid_columnconfigure(1,weight=0)
        window.grid_rowconfigure(0,weight=1)
        window.grid_rowconfigure(1,weight=1)
        window.grid_rowconfigure(2,weight=1)
        window.grid_rowconfigure(3,weight=0)
        window.grid_rowconfigure(4,weight=0)
        window.grid_rowconfigure(5,weight=0)
        self.labelt = tk.Label(window, text="Select Tables:", anchor="w", font="Arial 12 bold")
#        self.e = tk.Entry(window)
#        self.labele = tk.Label(window, text="Table Name:", anchor="w", font="Arial 12")
        self.s = tk.Scrollbar(window)
        self.labelt.grid(row=0,column=0,sticky='nsew')
#        self.labele.grid(row=1,column=0)
#       self.e.grid(row=1,column=0, sticky='w')
        self.s.grid(row=2,column=1,sticky='ns')
        vtable=['All']+table_dict_values
        
        qaGUI.p1 = args.parameter1
        qaGUI.p2 = args.parameter2
        qaGUI.p3 = args.parameter3
        qaGUI.p4 = args.parameter4
        
        qaGUI.od = args.outdirectory
        
        self.list_box = tk.Listbox(window, selectmode="multiple", listvariable=vtable)
        for i,j in zip(range(len(vtable)),vtable):
            if len(j) > self.len_max:
                self.len_max= len(j)
            self.list_box.insert(i, str(j))
        self.list_box.grid(row=2,column=0,sticky='nsew')
        self.s['command'] = self.list_box.yview
        self.list_box['yscrollcommand'] = self.s.set
        self.list_box.config(width=self.len_max)

        def on_closing():
            raise SystemExit
    
        master.protocol("WM_DELETE_WINDOW", on_closing)

        def var_window():
            window.withdraw()
            qaGUI.entered_table = self.e.get()
            ndex = self.list_box.curselection()
            qaGUI.selected_tables=[self.list_box.get(x) for x in ndex]
            var_win = tk.Toplevel()
            var_win.protocol("WM_DELETE_WINDOW", on_closing)
            var_win.grid_columnconfigure(0,weight=1)
            var_win.grid_columnconfigure(1,weight=0)
            var_win.grid_rowconfigure(0,weight=1)
            var_win.grid_rowconfigure(1,weight=1)
            var_win.grid_rowconfigure(2,weight=0)
            var_win.grid_rowconfigure(3,weight=0)
            labelv = tk.Label(var_win, text="Select Variables:", anchor="w",font="Arial 12 bold")
            labelv.grid(row=0,column=0)
            sv = tk.Scrollbar(var_win)
            sv.grid(row=1,column=1,sticky='ns')
            vvar=['All'] + fvariable1
            list_boxv = tk.Listbox(var_win, selectmode="multiple", listvariable=vvar)
            for i,j in zip(range(len(vvar)),vvar):
                list_boxv.insert(i, str(j))
            list_boxv.grid(row=1,column=0,sticky='nsew')
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
                
                list_params.protocol("WM_DELETE_WINDOW", on_closing)
                
                list_params.grid_columnconfigure(0,weight=1)
                list_params.grid_columnconfigure(1,weight=1)
                list_params.grid_rowconfigure(0,weight=1)
                list_params.grid_rowconfigure(1,weight=1)
                list_params.grid_rowconfigure(2,weight=1)
                list_params.grid_rowconfigure(3,weight=1)
                list_params.grid_rowconfigure(4,weight=1)
                list_params.grid_rowconfigure(5,weight=1)
                list_params.grid_rowconfigure(6,weight=1)
                list_params.grid_rowconfigure(7,weight=1)
                list_params.grid_rowconfigure(8,weight=1)
                list_params.grid_rowconfigure(9,weight=1)
                
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
                v3 = tk.StringVar()
                v4 = tk.StringVar()
                vod = tk.StringVar() 
              
               
                labelall = tk.Label(list_params, text="Current Selections:", anchor="w",font="Arial 12 bold")
                labeltables = tk.Label(list_params, text="Selected Tables:", anchor="w",font="Arial 10")
                labelvar = tk.Label(list_params, text="Selected Variables:", anchor="w",font="Arial 10")
                labelp1 = tk.Label(list_params, text="P1:", anchor="w",font="Arial 10")
                labelp2 = tk.Label(list_params, text="P2:", anchor="w",font="Arial 10")
                labelp3 = tk.Label(list_params, text="P3:", anchor="w",font="Arial 10")
                labelp4 = tk.Label(list_params, text="P4:", anchor="w",font="Arial 10")
                labelod = tk.Label(list_params, text="Out Directory:", anchor="w",font="Arial 10")
                
                labeltablesa = tk.Label(list_params, text=str(selected_tables).strip("[").strip("]").replace("'",""), anchor="w",font="Arial 10", wraplength=300)
                labelvara = tk.Label(list_params, text=str(selected_variables).strip("[").strip("]").replace("'",""), anchor="w",font="Arial 10", wraplength=300)
                labelp1a = tk.Label(list_params, textvariable=v1, anchor="w",font="Arial 10")
                labelp2a = tk.Label(list_params, textvariable=v2, anchor="w",font="Arial 10")
                labelp3a = tk.Label(list_params, textvariable=v3, anchor="w",font="Arial 10")
                labelp4a = tk.Label(list_params, textvariable=v4, anchor="w",font="Arial 10")
                labeloda = tk.Label(list_params, textvariable=vod, anchor="w",font="Arial 10")
                
                v1.set(qaGUI.p1)
                v2.set(qaGUI.p2)
                v3.set(qaGUI.p3)
                v4.set(qaGUI.p4)
                vod.set(qaGUI.od)
                
                labelall.grid(row=1,column=0)
                labeltables.grid(row=2,column=0)
                labelvar.grid(row=3,column=0)
                labelp1.grid(row=4,column=0)
                labelp2.grid(row=5,column=0)
                labelp3.grid(row=6,column=0)
                labelp4.grid(row=7,column=0)
                labelod.grid(row=8,column=0)                

                labeltablesa.grid(row=2,column=1)
                labelvara.grid(row=3,column=1)
                labelp1a.grid(row=4,column=1)
                labelp2a.grid(row=5,column=1)
                labelp3a.grid(row=6,column=1)
                labelp4a.grid(row=7,column=1) 
                labeloda.grid(row=8,column=1)                  
                
                def var_params():
                    list_params.withdraw()
                    var_par = tk.Toplevel()
                    
                    var_par.protocol("WM_DELETE_WINDOW", on_closing)
                    
                    var_par.grid_columnconfigure(0,weight=1)
                    var_par.grid_columnconfigure(1,weight=1)
                    var_par.grid_rowconfigure(0,weight=1)
                    var_par.grid_rowconfigure(1,weight=1)
                    var_par.grid_rowconfigure(2,weight=1)
                    var_par.grid_rowconfigure(3,weight=1)
                    var_par.grid_rowconfigure(4,weight=1)
                    var_par.grid_rowconfigure(5,weight=1)
                    
                    labelv = tk.Label(var_par, text="Enter Parameters:", anchor="w",font="Arial 12 bold")
                    labelv.grid(row=0,column=0, columnspan=2)
                    lp1 = tk.Label(var_par, text="Parameter 1:", anchor="w",font="Arial 10")
                    lp1.grid(row=1,column=0)
                    lp2 = tk.Label(var_par, text="Parameter 2:", anchor="w",font="Arial 10")
                    lp2.grid(row=2,column=0)
                    lp3 = tk.Label(var_par, text="Parameter 3:", anchor="w",font="Arial 10")
                    lp3.grid(row=3,column=0)
                    lp4 = tk.Label(var_par, text="Parameter 4:", anchor="w",font="Arial 10")
                    lp4.grid(row=4,column=0)
                    lod = tk.Label(var_par, text="Out Directory:", anchor="w",font="Arial 10")
                    lod.grid(row=5,column=0)
                    ep1 = tk.Entry(var_par)
                    ep1.grid(row=1,column=1, sticky='ew')
                    ep2 = tk.Entry(var_par)
                    ep2.grid(row=2,column=1, sticky='ew')
                    ep3 = tk.Entry(var_par)
                    ep3.grid(row=3,column=1, sticky='ew')
                    ep4 = tk.Entry(var_par)
                    ep4.grid(row=4,column=1, sticky='ew')
                    eod = tk.Entry(var_par)
                    eod.grid(row=5,column=1, sticky='ew')
        #            framep = tk.Frame(var_par)
        #            framep.grid(row=5,column=0, columnspan=2)
                    def close_par():
                        if ep1.get() !="":
                            qaGUI.p1=ep1.get()
                        if ep2.get() !="":
                            qaGUI.p2=ep2.get()
                        if ep3.get() !="":
                            qaGUI.p3=ep3.get()
                        if ep4.get() !="":                        
                            qaGUI.p4=ep4.get()
                        if eod.get() !="":
                            qaGUI.od=eod.get()
                        var_par.withdraw()
                        v1.set(qaGUI.p1)
                        v2.set(qaGUI.p2)
                        v3.set(qaGUI.p3)
                        v4.set(qaGUI.p4)
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
        self.e.grid(row=1,column=0, sticky='nsew')
#        self.button1 = tk.Button(self.frame, text = "Edit Parameters", command = var_params)
#        self.button1.grid(row=4,column=0)
        self.button = tk.Button(self.frame, text = "Next", command = var_window)
        self.button.grid(row=5,column=0)


#print(files)

#set parameters

class qaMain():
    outdataset=pd.DataFrame()  
        
    def q3(x):
        return x.quantile(.75)

    def spikefunction2(subset,var,a,j,cvar1="",cvar2="",cvar3="",cvar4=""):
        pd.options.mode.chained_assignment = 'raise'
    #    subset = subset.fillna(0)
        if 'estabs' in list(subset):
            subset.loc[(subset['estabs'].isna()) & (subset[j].isna()), j] = 0
            subset.loc[(subset['estabs']==0) & (subset[j].isna()), j] = 0
        if 'Estabs' in list(subset):
            subset.loc[(subset['Estabs'].isna()) & (subset[j].isna()), j] = 0
            subset.loc[(subset['Estabs']==0) & (subset[j].isna()), j] = 0
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
    
        f = {'abs_year2year': [qaMain.q3]}
        if cvar1 =="":
            q75=subset[["abs_year2year"]].agg(f)
            #!cvarref
            q75.columns = ["q3"]
            #!cvarref
            subset["q3"]=q75["q3"].item()
        if (cvar1 != "") & (cvar2 == ""):
            q75=subset[["abs_year2year",cvar1]].groupby([cvar1]).agg(f).reset_index()
            #!cvarref
            q75.columns = [cvar1,"q3"]
            #!cvarref
            subset=subset.merge(q75, on=[cvar1])
        if (cvar2 != "") & (cvar3 == ""):
            q75=subset[["abs_year2year",cvar1,cvar2]].groupby([cvar1,cvar2]).agg(f).reset_index()
            #!cvarref
            q75.columns = [cvar1,cvar2,"q3"]
            #!cvarref
            subset=subset.merge(q75, on=[cvar1,cvar2])
    
        if (cvar3 != "") & (cvar4 == ""):
            q75=subset[["abs_year2year",cvar1,cvar2,cvar3]].groupby([cvar1,cvar2,cvar3]).agg(f).reset_index()
            #!cvarref
            q75.columns = [cvar1,cvar2,cvar3,"q3"]
            #!cvarref
            subset=subset.merge(q75, on=[cvar1,cvar2,cvar3])    
    
        if cvar4 != "":
            q75=subset[["abs_year2year",cvar1,cvar2,cvar3,cvar4]].groupby([cvar1,cvar2,cvar3,cvar4]).agg(f).reset_index()
            #!cvarref
            q75.columns = [cvar1,cvar2,cvar3,cvar4,"q3"]
            #!cvarref
            subset=subset.merge(q75, on=[cvar1,cvar2,cvar3,cvar4])
    
    
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
        if cvar1 =="":
            subset.loc[:,"Last"] = 0      
            #!cvarref    
            last_row_index = subset.tail(1).index.values             
            subset.loc[last_row_index, "Last"] = 1        
            subset.loc[last_row_index, "op"] = 0  
            subset.loc[last_row_index, "sc"] = 0        
            subset.loc[last_row_index, "sf"] = 0
                                      
            subset.loc[:,"First"] = 0   
            #!cvarref
            first_row_index = subset.head(1).index.values             
            subset.loc[first_row_index, "First"] = 1        
            subset.loc[first_row_index, "op"] = 0
            subset.loc[first_row_index, "sc"] = 0        
            subset.loc[first_row_index, "sf"] = 0         
        
        if (cvar1 != "") & (cvar2 == ""):
            subset.loc[:,"Last"] = 0      
            #!cvarref    
            last_row_index = subset.groupby([cvar1]).tail(1).index.values             
            subset.loc[last_row_index, "Last"] = 1        
            subset.loc[last_row_index, "op"] = 0  
            subset.loc[last_row_index, "sc"] = 0        
            subset.loc[last_row_index, "sf"] = 0
                                      
            subset.loc[:,"First"] = 0   
            #!cvarref
            first_row_index = subset.groupby([cvar1]).head(1).index.values             
            subset.loc[first_row_index, "First"] = 1        
            subset.loc[first_row_index, "op"] = 0
            subset.loc[first_row_index, "sc"] = 0        
            subset.loc[first_row_index, "sf"] = 0  
        
        if (cvar2 != "") & (cvar3 == ""):
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
            subset.loc[first_row_index, "sc"] = 0        
            subset.loc[first_row_index, "sf"] = 0 
            
        if (cvar3 != "") & (cvar4 == ""):
            subset.loc[:,"Last"] = 0 
            #!cvarref    
            last_row_index = subset.groupby([cvar1,cvar2,cvar3]).tail(1).index.values             
            subset.loc[last_row_index, "Last"] = 1        
            subset.loc[last_row_index, "op"] = 0                                
            subset.loc[:,"First"] = 0   
            #!cvarref
            first_row_index = subset.groupby([cvar1,cvar2,cvar3]).head(1).index.values             
            subset.loc[first_row_index, "First"] = 1        
            subset.loc[first_row_index, "op"] = 0
            subset.loc[first_row_index, "sc"] = 0        
            subset.loc[first_row_index, "sf"] = 0 
    
        if cvar4 != "":
            subset.loc[:,"Last"] = 0 
            #!cvarref    
            last_row_index = subset.groupby([cvar1,cvar2,cvar3,cvar4]).tail(1).index.values             
            subset.loc[last_row_index, "Last"] = 1        
            subset.loc[last_row_index, "op"] = 0                                
            subset.loc[:,"First"] = 0   
            #!cvarref
            first_row_index = subset.groupby([cvar1,cvar2,cvar3,cvar4]).head(1).index.values             
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
        subset.loc[(subset["sc"] != subset["sf"]) & (subset["abs_year2yearp2"] < subset["abs_year2yearp1"]*p4) & (subset["First"] == 1), "op" ] += 1
        
        #last adjustments
        subset.loc[(subset["abs_year2year"] > p1*subset["q3"]) & (subset["Last"] == 1), "op"] += 1        
        subset.loc[(subset["ntm1"] !=0) & (subset["abs_year2year"]/subset["ntm1"] > p2) & (subset["Last"] == 1), "op"] += 1        
        subset.loc[(subset["ntm1"] ==0) & (subset["Last"] == 1), "op"] += 1        
        subset.loc[(subset["abs_year2year"] > p3) & (subset["Last"] == 1), "op"] += 1        
        subset.loc[(subset["year2year"]>=0) & (subset["Last"] == 1), "sc"] = 1        
        subset.loc[(subset["year2yearm1"]>=0) & (subset["Last"] == 1), "sf"] = 1        
        subset.loc[(subset["sc"] == subset["sf"]) & (subset["Last"] == 1), "op" ] += 1        
        subset.loc[(subset["sc"] != subset["sf"]) & (subset["abs_year2yearm1"] < subset["abs_year2year"]*p4) & (subset["Last"] == 1), "op" ] += 1
        
        #special rules
        #!cvarref
        if cvar1 == "fage4" or cvar2 == "fage4" or cvar3 == "fage4":
            subset.loc[(subset["fage4"]=="g) 6 to 10") & (subset["year2"]<=1987), "op"]=-1
            subset.loc[(subset["fage4"]=="h) 11 to 15") & (subset["year2"]<=1992), "op"]=-1
            subset.loc[(subset["fage4"]=="i) 16 to 20") & (subset["year2"]<=1997), "op"]=-1 
            subset.loc[(subset["fage4"]=="j) 21 to 25") & (subset["year2"]<=2002), "op"]=-1                    
        if cvar1 == "Fage4" or cvar2 == "Fage4" or cvar3 == "Fage4":
            subset.loc[(subset["Fage4"]=="g) 6 to 10") & (subset["year2"]<=1987), "op"]=-1
            subset.loc[(subset["Fage4"]=="h) 11 to 15") & (subset["year2"]<=1992), "op"]=-1
            subset.loc[(subset["Fage4"]=="i) 16 to 20") & (subset["year2"]<=1997), "op"]=-1 
            subset.loc[(subset["Fage4"]=="j) 21 to 25") & (subset["year2"]<=2002), "op"]=-1  
            
    #    print(subset[['year2',j,'year2year','year2yearp1','year2yearp2','sc','sf','op']])
         
        #check for outliers
        subset.loc[:,"spike"]=0
        subset.loc[subset["op"]>3, "spike"]=1
        #!cvarref
        spikesum1=0

        if cvar1 == "":
            spikesum1 = subset["spike"].sum() 
        
        if (cvar1 != "") & (cvar2 == ""):
            spikesum = subset[[cvar1,"spike"]].groupby([cvar1]).sum().reset_index()
            spikesum = spikesum.loc[spikesum["spike"]>=1]
    
        if (cvar2 != "") & (cvar3 == ""):
            spikesum = subset[[cvar1,cvar2,"spike"]].groupby([cvar1,cvar2]).sum().reset_index()
            spikesum = spikesum.loc[spikesum["spike"]>=1]
            
        if (cvar3 != "") & (cvar4 == ""):
            spikesum = subset[[cvar1,cvar2,cvar3,"spike"]].groupby([cvar1,cvar2,cvar3]).sum().reset_index()
            spikesum = spikesum.loc[spikesum["spike"]>=1]
            
        if cvar4 != "":
            spikesum = subset[[cvar1,cvar2,cvar3,cvar4,"spike"]].groupby([cvar1,cvar2,cvar3,cvar4]).sum().reset_index()
            spikesum = spikesum.loc[spikesum["spike"]>=1]   

#rightbackhere
        if "msa" in [cvar1,cvar2,cvar3,cvar4]:
            lmsa=pd.read_csv(ldirectory+"msacodes_names.csv")
            subset=subset.merge(lmsa, left_on="msa", right_on="msa_num")
            subset["msa"]=subset["label"]
            spikesum=spikesum.merge(lmsa, left_on="msa", right_on="msa_num")
            spikesum["msa"]=spikesum["label"]
        if "Msa" in [cvar1,cvar2,cvar3,cvar4]:
            lmsa=pd.read_csv(ldirectory+"msacodes_names.csv")
            subset=subset.merge(lmsa, left_on="Msa", right_on="msa_num")
            subset["Msa"]=subset["label"]
            spikesum=spikesum.merge(lmsa, left_on="Msa", right_on="msa_num")
            spikesum["Msa"]=spikesum["label"]
        if "state" in [cvar1,cvar2,cvar3,cvar4]:
            lmsa=pd.read_csv(ldirectory+"state_fips_region_division.csv")
            subset=subset.merge(lmsa, left_on="state", right_on="state_fips")
            subset["state"]=subset["state_name"]
            spikesum=spikesum.merge(lmsa, left_on="state", right_on="state_fips")
            spikesum["state"]=spikesum["state_name"]
        if "State" in [cvar1,cvar2,cvar3,cvar4]:
            subset=subset.merge(lmsa, left_on="State", right_on="state_fips")
            subset["State"]=subset["state_name"]
            lmsa=pd.read_csv(ldirectory+"state_fips_region_division.csv")
            spikesum=spikesum.merge(lmsa, left_on="State", right_on="state_fips")
            spikesum["State"]=spikesum["state_name"]
        
        if cvar1 == "":
            outset = subset.loc[subset["spike"]==1][["ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1"]]
        if (cvar1 != "") & (cvar2 == ""):
            outset = subset.loc[subset["spike"]==1][[cvar1,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1"]]
        if (cvar2 != "") & (cvar3 == ""):
            outset = subset.loc[subset["spike"]==1][[cvar1,cvar2,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1"]]
        if (cvar3 != "") & (cvar4 == ""):
            outset = subset.loc[subset["spike"]==1][[cvar1,cvar2,cvar3,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1"]]
        if cvar4 != "":
            outset = subset.loc[subset["spike"]==1][[cvar1,cvar2,cvar3,cvar4,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1"]]
        outset["table"]=a
        #!cvarref
        textparameter = "Flagged years reflect where absolute value of change PY to CY is all of the following:"+"""
"""+"greater than " + str(int(p1)) +" times p75;"+" greater than "+str(int(p2*100))+"%; greater than "+str(int(p3))+"; followed by "+str(int(p4*100))+"% or more reversal."
        
        outdata=pd.DataFrame()
        
        if (cvar1 == "") & (spikesum1>0) & (cvar2 ==""):
            outset = subset.loc[subset["spike"]==1][["year2","ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1","spike"]]
            outset["table"]=a
            outdata=outdata.append(outset,sort=False)
            x = subset["year2"]
            y = subset[j]
            x2 =subset.loc[subset["spike"]==1, "year2"]
            v = subset.loc[subset["spike"]==1, j]
            
            plt.plot(x, y, marker='o', markersize=3)
            plt.plot(x2,v,'ro')    
            plt.title(str(a).replace(".csv","")+"""
"""+str(j),loc='center')
            plt.ylabel(j)
            plt.xlabel("Year")
            ticks = np.arange(min(x), max(x)+1,step=2)
            if ((max(x) % 2) == 0) & ((min(x) % 2) != 0):
                ticks = np.arange(min(x)+1, max(x)+1,step=2)
            if ((max(x) % 2) != 0) & ((min(x) % 2) == 0):
                ticks = np.arange(min(x)+1, max(x)+1,step=2)
#            ticks = list(set().union(np.arange(min(x), max(x)+1,step=2), [min(x),max(x)]))
            plt.xticks(ticks, rotation=90)
            
            plt.annotate(textparameter, (0,0), (0,-48), 'axes fraction', textcoords='offset points', va='top', size = 6)
            
            plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))            
            
            plt.tight_layout(pad=1.5)
            
            filestring = odirectory+str(a).replace(".csv","")+"."+str(j)+".png"
            filestring = filestring.replace(" ","_").replace(")","")
            print("Outlier found in "+str(a).replace(".csv","")+". Writing "+str(filestring))
            plt.savefig(filestring)
            plt.clf()
            
        if (cvar1 != "") & (cvar2 == ""):
            for z in list(spikesum[cvar1]):
                outset = subset.loc[subset[cvar1]==z][["year2",cvar1,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1","spike"]]
                outset["table"]=a
                outdata=outdata.append(outset,sort=False)
            #print(str(q)+str(z))
                x = subset.loc[(subset[cvar1]==z), "year2"]
                y = subset.loc[(subset[cvar1]==z), j]
                x2 =subset.loc[(subset[cvar1]==z) & (subset["spike"]>=1), "year2"]
                v = subset.loc[(subset[cvar1]==z) & (subset["spike"]>=1), j]
                
                plt.plot(x, y, marker='o', markersize=3)
                plt.plot(x2,v,'ro')    
                
                plt.title(str(a).replace(".csv","")+"""
"""+cvar1+": "+str(z)+"""
"""+str(j),loc='center')
                plt.ylabel(j)
                plt.xlabel("Year")
                ticks = np.arange(min(x), max(x)+1,step=2)
                if ((max(x) % 2) == 0) & ((min(x) % 2) != 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                if ((max(x) % 2) != 0) & ((min(x) % 2) == 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                plt.xticks(ticks, rotation=90)

                plt.annotate(textparameter, (0,0), (0,-48), 'axes fraction', textcoords='offset points', va='top', size = 6)
                            
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))        

                plt.tight_layout(pad=1.5)
                
                filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(z)+"."+str(j)+".png"
                filestring = filestring.replace(" ","_").replace(")","")
                print("Outlier found in "+str(a).replace(".csv","")+". Writing "+str(filestring))
                plt.savefig(filestring)
                plt.clf()
    
        if (cvar2 != "") & (cvar3 == ""):
            for q,z in list(zip(spikesum[cvar1],spikesum[cvar2])):
                outset = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z)][["year2",cvar1,cvar2,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1","spike"]]
                outset["table"]=a
                outdata=outdata.append(outset,sort=False)
                x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z), "year2"]
                y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z), j]
                x2 =subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["spike"]>=1), "year2"]
                v = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset["spike"]>=1), j]
                
                plt.plot(x, y, marker='o', markersize=3)
                plt.plot(x2,v,'ro')
                
                plt.title(str(a).replace(".csv","")+"""
"""+cvar1+": "+str(q)+"""
"""+cvar2+": "+str(z)+"""
"""+str(j),loc='center')
                plt.ylabel(j)
                plt.xlabel("Year")
                ticks = np.arange(min(x), max(x)+1,step=2)
                if ((max(x) % 2) == 0) & ((min(x) % 2) != 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                if ((max(x) % 2) != 0) & ((min(x) % 2) == 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                plt.xticks(ticks, rotation=90)
                
                plt.annotate(textparameter, (0,0), (0,-48), 'axes fraction', textcoords='offset points', va='top', size = 6)
                
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))  

                plt.tight_layout(pad=1.5)
                filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(q)+"."+cvar2+"_"+str(z)+"."+str(j)+".png"
                filestring = filestring.replace(" ","_").replace(")","")
                print("Outlier found in "+str(a).replace(".csv","")+". Writing "+str(filestring))
                plt.savefig(filestring)
                plt.clf()            
    
        if (cvar3 != "") & (cvar4 == ""):
            for q,z,o in list(zip(spikesum[cvar1],spikesum[cvar2],spikesum[cvar3])):
                outset = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o)][["year2",cvar1,cvar2,cvar3,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1","spike"]]
                outset["table"]=a
                outdata=outdata.append(outset,sort=False)
                #print(str(q)+str(z))
                x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o), "year2"]
                y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o), j]
                x2 =subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset["spike"]>=1), "year2"]
                v = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset["spike"]>=1), j]
                
                plt.plot(x, y, marker='o', markersize=3)
                plt.plot(x2,v,'ro')
                
                plt.title(str(a).replace(".csv","")+"""
"""+cvar1+": "+str(q)+"""
"""+cvar2+": "+str(z)+"""
"""+cvar3+": "+str(o)+"""
"""+str(j),loc='center')
                plt.ylabel(j)
                plt.xlabel("Year")
                ticks = np.arange(min(x), max(x)+1,step=2)
                if ((max(x) % 2) == 0) & ((min(x) % 2) != 0):
                    ticks = np.arange(min(x)+1, max(x)+2,step=2)
                if ((max(x) % 2) != 0) & ((min(x) % 2) == 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                plt.xticks(ticks, rotation=90)
                
                plt.annotate(textparameter, (0,0), (0,-48), 'axes fraction', textcoords='offset points', va='top', size = 6)
                
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))  

                plt.tight_layout(pad=1.5)
                filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(q)+"."+cvar2+"_"+str(z)+"."+cvar3+"_"+str(o)+"."+str(j)+".png"
                filestring = filestring.replace(" ","_").replace(")","")
                print("Outlier found in "+str(a).replace(".csv","")+". Writing "+str(filestring))
                plt.savefig(filestring)
                plt.clf()
    
        if cvar4 != "":
            for q,z,o,p in list(zip(spikesum[cvar1],spikesum[cvar2],spikesum[cvar3],spikesum[cvar4])):
                outset = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p)][["year2",cvar1,cvar2,cvar4,"ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1","spike"]]
                outset["table"]=a
                outdata=outdata.append(outset,sort=False)
                #print(str(q)+str(z))
                x = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p), "year2"]
                y = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p), j]
                x2 =subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p) & (subset["spike"]>=1), "year2"]
                v = subset.loc[(subset[cvar1]==q) & (subset[cvar2]==z) & (subset[cvar3]==o) & (subset[cvar4]==p) & (subset["spike"]>=1), j]
                
                plt.plot(x, y, marker='o', markersize=3)
                plt.plot(x2,v,'ro')
                
                plt.title(str(a).replace(".csv","")+"""
"""+cvar1+": "+str(q)+"""
"""+cvar2+": "+str(z)+"""
"""+cvar3+": "+str(o)+"""
"""+cvar4+": "+str(p)+"""
"""+str(j),loc='center')
                plt.ylabel(j)
                plt.xlabel("Year")
                ticks = np.arange(min(x), max(x)+1,step=2)
                if ((max(x) % 2) == 0) & ((min(x) % 2) != 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                if ((max(x) % 2) != 0) & ((min(x) % 2) == 0):
                    ticks = np.arange(min(x)+1, max(x)+1,step=2)
                plt.xticks(ticks, rotation=90)
                
                plt.annotate(textparameter, (0,0), (0,-48), 'axes fraction', textcoords='offset points', va='top', size = 6)
                
                plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))  

                plt.tight_layout(pad=1.5)
                
                filestring = odirectory+str(a).replace(".csv","")+"."+cvar1+"_"+str(q)+"."+cvar2+"_"+str(z)+"."+cvar3+"_"+str(o)+"."+cvar4+"_"+str(p)+"."+str(j)+".png"
                filestring = filestring.replace(" ","_").replace(")","")
                print("Outlier found in "+str(a).replace(".csv","")+". Writing "+str(filestring))
                plt.savefig(filestring)
                plt.clf()
#        print(outset)
#        print(qaMain.outdataset)
#        qaMain.outdataset=qaMain.outdataset.append(outset, sort=False)
#        print(qaMain.outdataset)
        sortlist = ["table",cvar1,cvar2,cvar3,cvar4,"year2","ntm1",var,"ntp1","year2yearm1","year2year","year2yearp1","spike"]
        orderlist = []
        for i in sortlist:
            if i in list(outdata):
                orderlist.append(i)
        if not outdata.empty:
            outdata = outdata[orderlist]
            outdata.to_csv(odirectory+"outliers_"+str(a)+"_"+str(j)+"_"+str(dt.datetime.now()).replace(" ","_")+".csv")
            print(str(outdata["table"].count())+" outliers found in "+str(a)+" for "+str(j))
        else:
            print("0 outliers found in "+str(a)+" for "+str(j))
        if args.testing == 1:
            print(spikesum)
    
    def __init__(self,ddirectory,selected_tables,selected_variables):
        self.ddirectory=ddirectory
        self.selected_tables=selected_tables
        self.selected_variables = selected_variables
        self.selected_variables1 = [item.lower() for item in selected_variables]
        self.catlist1=["fage4","ifsize","metro","fsize","state","sic1","msa","Fage4","Ifsize","Metro","Fsize","State","Sic1","Msa","age4","Age4","size","Size","isize","Isize"]        
        for z in self.selected_tables:   
            dfile = z 
            data = pd.read_csv(self.ddirectory+dfile+".csv")
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
        
        #    if varnin == 'all':    
        #        for i,j in zip(fvariable1,fvariable2):
        #            if i in list(data):
        #                fvariable.append(i)
        #            if j in list(data):
        #                fvariable.append(j)
        #    else:
        #        assert varnin in fvariable1+fvariable2, "Variable name not valid"
        #        if varnin not in list(data):
        #            if varnin.istitle():
        #                var = varnin.lower()
        #            else:
        #                var = varnin.capitalize()
        #        else:
        #            var = varnin
        #        assert var in list(data), "Variable name not valid for table " + z
        #        fvariable = [var]
        #        lvariable=list(data)
        #    ci=len(set(list(data)) & set(catlist1))
            cilist=list(set(list(data)) & set(self.catlist1))
            def removelist(datax,x):
                return [value for value in x if datax[value].isnull().all() == False]
            cilist= removelist(data, cilist)
            ci = len(cilist)
#            print(z)
#            print(ci)
                            #run analysis on subset data        
                            #calculations
        #no variable tables
            if ci ==0:
                for j in fvariable:
                    var = j
                    data.sort_values("year2", inplace=True) 
                    qaMain.spikefunction2(data,var,z,j)
        #one variable tables
            if ci==1:
                cvar=cilist[0]
                for j in fvariable:
                    var = j
                    data.sort_values([cvar,"year2"], inplace=True)            
                    qaMain.spikefunction2(data,var,z,j,cvar)
        
        #two variable tables
            if ci==2:
                cvar=cilist[0]
                cvar2=cilist[1]   
                #subset values
                for j in fvariable:
                    var = j
                    data.sort_values([cvar,cvar2,"year2"], inplace=True)         
                    qaMain.spikefunction2(data,var,z,j,cvar,cvar2)
        #three variable tables
            if ci==3:
                cvar=cilist[0]
                cvar2=cilist[1]
                cvar3=cilist[2]
                #subset values
                for j in fvariable:
                    var = j
                    data.sort_values([cvar,cvar2,cvar3,"year2"], inplace=True)          
                    qaMain.spikefunction2(data,var,z,j,cvar,cvar2,cvar3)
        
        #four variable tables
            if ci==4:
                cvar=cilist[0]
                cvar2=cilist[1]
                cvar3=cilist[2]
                cvar4=cilist[3]
                #subset values
                for j in fvariable:
                    var = j
                    data.sort_values([cvar,cvar2,cvar3,cvar4,"year2"], inplace=True)          
                    qaMain.spikefunction2(data,var,z,j,cvar,cvar2,cvar3,cvar4)
#        qaMain.outdataset.to_csv(odirectory+"outliers_"+str(dt.datetime.now()).replace(" ","_")+".csv")

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
#    parser.add_argument('--table','-t', help="Table input use 'all' for all tables in directory",type = str, default = 'all')
    parser.add_argument('--parameter1', '-p1', help="First Parameter defined in Section E", type = float, default = 5)
    parser.add_argument('--parameter2', '-p2', help="Second Parameter defined in Section E", type = float, default = .05)
    parser.add_argument('--parameter3', '-p3', help="Third Parameter defined in Section E", type = float, default = 10000)
    parser.add_argument('--parameter4', '-p4', help="Fourth Parameter defined in Section E", type = float, default = .8)
#    parser.add_argument('--varn', '-vn', help="Variable to run through QA", type = str, default = 'all')
    
    parser.add_argument('--datadirectory', '-dd', help="Directory where data is stored", type = str, default = datadirectorystr)
    parser.add_argument('--lookupdirectory', '-ld', help="Directory where lookup lists are stored", type = str, default = lookupdirectorystr)
    parser.add_argument('--outdirectory', '-od', help="Directory where output files are write", type = str, default = outdirectorystr)
    parser.add_argument('--testing', '-t', help="Indicates if being run with testing set, 1 for testing", type = int, default = 0)
    args = parser.parse_args()


    #read in data table
    ddirectory = args.datadirectory
    ldirectory = args.lookupdirectory
    odirectory= args.outdirectory 
    
    
    table_dict = { 'bds_f_all_release.csv': ['bds_f_all_release', 1]  ,
 'bds_e_all_release.csv': ['bds_e_all_release', 2]  ,
 'bds_f_sic_release.csv': ['bds_f_sic_release', 3]  ,
 'bds_e_sic_release.csv': ['bds_e_sic_release', 4]  ,
 'bds_f_sz_release.csv': ['bds_f_sz_release', 5]  ,
 'bds_e_sz_release.csv': ['bds_e_sz_release', 6]  ,
 'bds_f_isz_release.csv': ['bds_f_isz_release', 7]  ,
 'bds_e_isz_release.csv': ['bds_e_isz_release', 8]  ,
 'bds_f_age_release.csv': ['bds_f_age_release', 9]  ,
 'bds_e_age_release.csv': ['bds_e_age_release', 10]  ,
 'bds_f_st_release.csv': ['bds_f_st_release', 11]  ,
 'bds_e_st_release.csv': ['bds_e_st_release', 12]  ,
 'bds_f_metrononmetro_release.csv': ['bds_f_metrononmetro_release', 13]  ,
 'bds_f_msa_release.csv': ['bds_f_msa_release', 14]  ,
 'bds_e_msa_release.csv': ['bds_e_msa_release', 15]  ,
 'bds_f_agesz_release.csv': ['bds_f_agesz_release', 16]  ,
 'bds_e_agesz_release.csv': ['bds_e_agesz_release', 17]  ,
 'bds_f_ageisz_release.csv': ['bds_f_ageisz_release', 18]  ,
 'bds_e_ageisz_release.csv': ['bds_e_ageisz_release', 19]  ,
 'bds_f_agesic_release.csv': ['bds_f_agesic_release', 20]  ,
 'bds_e_agesic_release.csv': ['bds_e_agesic_release', 21]  ,
 'bds_f_agemetrononmetro_release.csv': ['bds_f_agemetrononmetro_release', 22]  ,
 'bds_f_agemsa_release.csv': ['bds_f_agemsa_release', 23]  ,
 'bds_f_agest_release.csv': ['bds_f_agest_release', 24]  ,
 'bds_e_agest_release.csv': ['bds_e_agest_release', 25]  ,
 'bds_f_szsic_release.csv': ['bds_f_szsic_release', 26]  ,
 'bds_e_szsic_release.csv': ['bds_e_szsic_release', 27]  ,
 'bds_f_szmetrononmetro_release.csv': ['bds_f_szmetrononmetro_release', 28]  ,
 'bds_f_szmsa_release.csv': ['bds_f_szmsa_release', 29]  ,
 'bds_f_szst_release.csv': ['bds_f_szst_release', 30]  ,
 'bds_e_szst_release.csv': ['bds_e_szst_release', 31]  ,
 'bds_f_iszsic_release.csv': ['bds_f_iszsic_release', 32]  ,
 'bds_e_iszsic_release.csv': ['bds_e_iszsic_release', 33]  ,
 'bds_f_iszmetrononmetro_release.csv': ['bds_f_iszmetrononmetro_release', 34]  ,
 'bds_f_iszst_release.csv': ['bds_f_iszst_release', 35]  ,
 'bds_e_iszst_release.csv': ['bds_e_iszst_release', 36]  ,
 'bds_f_agesz_sic_release.csv': ['bds_f_agesz_sic_release', 37]  ,
 'bds_e_agesz_sic_release.csv': ['bds_e_agesz_sic_release', 38]  ,
 'bds_f_agesz_st_release.csv': ['bds_f_agesz_st_release', 39]  ,
 'bds_e_agesz_st_release.csv': ['bds_e_agesz_st_release', 40]  ,
 'bds_f_ageszmetrononmetro_release.csv': ['bds_f_ageszmetrononmetro_release', 41]  ,
 'bds_f_agesz_msa_release.csv': ['bds_f_agesz_msa_release', 42]  ,
 'bds_f_ageisz_sic_release.csv': ['bds_f_ageisz_sic_release', 43]  ,
 'bds_e_ageisz_sic_release.csv': ['bds_e_ageisz_sic_release', 44]  ,
 'bds_f_ageisz_st_release.csv': ['bds_f_ageisz_st_release', 45]  ,
 'bds_e_ageisz_st_release.csv': ['bds_e_ageisz_st_release', 46]  ,
 'bds_f_ageiszmetro_release.csv': ['bds_f_ageiszmetro_release', 47]  ,
 'bds_f_ageszmetro_state_release.csv': ['bds_f_ageszmetro_state_release', 48]  ,
 'bds_f_ageiszmetro_state_release.csv': ['bds_f_ageiszmetro_state_release', 49]  }    
    
    files = [f for f in os.listdir(ddirectory) if os.path.isfile(os.path.join(ddirectory,f))]
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
    p3 = args.parameter3
    p4 = args.parameter4    
    
    master = tk.Tk()
    window = qaGUI(master)
 
    def on_closing():
        raise SystemExit
    
    master.protocol("WM_DELETE_WINDOW", on_closing)
    
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
    try: window.p3
    except AttributeError: window.p3 = None
    if window.p3 != None:
        if float(window.p3) !="":
            p3 = float(window.p3)
    try: window.p4
    except AttributeError: window.p4 = None
    if window.p4 != None:
        if float(window.p4) !="":
            p4 = float(window.p4)
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
       

    print("Tables Selected:")
    print(selected_tables)
    print("Variables Selected:")
    print(selected_variables)
    
    
    qaMain(ddirectory,selected_tables,selected_variables)    
    
    
        
    
totaltime=time.time() - start_time
skiptime=time2-time1

print("--- %s seconds ---" % (totaltime-skiptime))