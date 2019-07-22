# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 12:52:52 2019

@author: tibeg
"""

#create gui for everything
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

datadirectorystr = 'C:/Users/tibeg/Documents/ewdwork/datatables'
lookupdirectorystr =  'C:/Users/tibeg/Documents/ewdwork/high_level'
outdirectorystr= 'C:/Users/tibeg/Documents/ewdwork/output'

#datadirectorystr = '/lbd/bitsi/ewdwork/datatables/'
#lookupdirectorystr =  '/lbd/bitsi/ewdwork/data/'
#outdirectorystr= '/lbd/bitsi/ewdwork/output/'

#main gui for program
class qaGUI:
    def __init__(self,window):
        #clear a the main list_box selections
        def clear_list():
            qaGUI.list_box.delete(0, tk.END)
        #close all the windows replaced with internal function in list_params
#        def close_all():
#            window.destroy()
        #restart program will only work in linux
        def restart():
            python = sys.executable
            os.execl(python, python, * sys.argv)      
        def handle_focus_in():
            labeloda.delete(0,tk.END)
            labeloda.config(fg='black')
        def handle_focus_out():
            labeloda.delete(0,tk.END)
            labeloda.config(fg='grey')
            labeloda.insert(0,qaGUI.vod.get())
        def handle_enter(txt):
            handle_focus_out('example')
        #open selection confirmation screen
        def open_confirm():
            def close_all_p():
                qaGUI.od = labeloda.get()
                qaGUI.selected_tables = selected_tables
                window.destroy()
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
            
            ndex = qaGUI.list_box.curselection()
            qaGUI.selected_tables=[qaGUI.list_box.get(x) for x in ndex]
            qaGUI.entered_tables = qaGUI.e.get()
            selected_tables= qaGUI.selected_tables
            entered_tables= qaGUI.entered_tables
            if selected_tables == []:
                if entered_tables == "":
                    selected_tables = "All"
            if entered_tables != "":
                selected_tables = entered_tables.replace(" ","").split(",") + selected_tables
            if 'All' in selected_tables:
                selected_tables = "All" 
            
            selected_variables = variable_selection()
            if selected_variables == []:
                    selected_variables = "All"    
            if 'All' in selected_variables:
                selected_variables = "All"

            vod = tk.StringVar() 

           
            labelall = tk.Label(list_params, text="Current Selections:", anchor="w",font="Arial 12 bold")
            labeltables = tk.Label(list_params, text="Selected Tables:", anchor="w",font="Arial 10")
            labelvar = tk.Label(list_params, text="Selected Variables:", anchor="w",font="Arial 10")
            labelod = tk.Label(list_params, text="Out Directory:", anchor="w",font="Arial 10")
            
            labeltablesa = tk.Label(list_params, text=str(selected_tables).strip("[").strip("]").replace("'",""), anchor="w",font="Arial 10", wraplength=300)
            labelvara = tk.Label(list_params, text=str(selected_variables).strip("[").strip("]").replace("'",""), anchor="w",font="Arial 10", wraplength=300)
            labeloda = tk.Entry(list_params, fg='grey',font="Arial 10",width=len(qaGUI.vod.get()))
            #labeloda = tk.Label(list_params, textvariable=vod, anchor="w",font="Arial 10")
            
            vod.set(qaGUI.od)
            
            labelall.grid(row=1,column=0)
            labeltables.grid(row=2,column=0)
            labelvar.grid(row=3,column=0)
            labelod.grid(row=8,column=0)     
            
            labeloda.insert(0,qaGUI.vod.get())
            
            labeloda.bind("<FocusIn>", handle_focus_in)
            labeloda.bind("<FocusOut>", handle_focus_in)
            labeloda.bind("<Return>", handle_enter)
            
            labeltablesa.grid(row=2,column=1)
            labelvara.grid(row=3,column=1)
            labeloda.grid(row=8,column=1,sticky='e')    
            
            buttona = tk.Button(list_params, text = "Submit", command = close_all_p)
            buttona.grid(row=9,column=0, columnspan=1)
            buttonr = tk.Button(list_params, text = "Restart", command = restart)
            buttonr.grid(row=9,column=1, columnspan=1)            
        #fill list box datatables
        def fill_list():
            ddirectory=qaGUI.vdd.get()
            files = [f for f in os.listdir(ddirectory) if os.path.isfile(os.path.join(ddirectory,f))]
            for f in list(table_dict.keys()):
                if f not in files:
                    del table_dict[f]    
            for f in files:
                if f not in list(table_dict.keys()):
                    table_dict.update({f:[f.replace(".csv",""),len(table_dict)+1]})
            table_dict_values = [table_dict[i][0] for i in table_dict.keys()]
            vtable=['All']+table_dict_values
            qaGUI.list_box = tk.Listbox(window, selectmode="multiple", listvariable=vtable)
            for i,j in zip(range(len(vtable)),vtable):
                if len(j) > qaGUI.len_max:
                    qaGUI.len_max= len(j)
                qaGUI.list_box.insert(i, str(j))
            self.list_box.grid(row=2,column=0,sticky='nsew')
            self.s['command'] = self.list_box.yview
            self.list_box['yscrollcommand'] = self.s.set
            self.list_box.config(width=self.len_max)
        #system close on close window    
        def on_closing():
            raise SystemExit
        window.protocol("WM_DELETE_WINDOW", on_closing)
        #open data folder editor
        def edit_folder(window):
            def close_par(window):
                if eod.get() !="":
                    qaGUI.dd=eod.get()
                var_par.withdraw()
                qaGUI.vdd.set(qaGUI.dd)
                clear_list()
                window.deiconify()
                fill_list()
            window.withdraw()
            var_par = tk.Toplevel()
            var_par.protocol("WM_DELETE_WINDOW", on_closing)
            var_par.grid_columnconfigure(0,weight=1)
            var_par.grid_columnconfigure(1,weight=1)
            var_par.grid_rowconfigure(0,weight=1)
            var_par.grid_rowconfigure(1,weight=1)
            labelv = tk.Label(var_par, text="Enter Parameters:", anchor="w",font="Arial 12 bold")
            labelv.grid(row=0,column=0, columnspan=2)
            lod = tk.Label(var_par, text="Data Directory:", anchor="w",font="Arial 10")
            lod.grid(row=5,column=0)
            eod = tk.Entry(var_par)
            eod.grid(row=5,column=1, sticky='ew')
#            framep = tk.Frame(var_par)
#            framep.grid(row=5,column=0, columnspan=2)
            buttonv = tk.Button(var_par, text = "Submit", command = lambda: close_par(window))
            buttonv.grid(row=6,column=0, columnspan=2)
        

        #open Variable selector and high data
        def var_window():
            #close variable window and collect selections
            def close_var():
                ndexcbp = list_boxcbp.curselection()
                qaGUI.selected_variablescbp=[list_boxcbp.get(x) for x in ndexcbp]
                ndexbed = list_boxbed.curselection()
                qaGUI.selected_variablesbed=[list_boxbed.get(x) for x in ndexbed]
                ndexbits = list_boxbits.curselection()
                qaGUI.selected_variablesbits=[list_boxbits.get(x) for x in ndexbits]
                ndexbds = list_boxbds.curselection()
                qaGUI.selected_variablesbds=[list_boxbds.get(x) for x in ndexbds]
                var_select.withdraw()
                open_confirm()
            def create_listbox(var,r,c,var_list):
                label = tk.Label(var_select, text=var, anchor="w",font="Arial 10 bold")
                label.grid(row=r,column=c)
                s = tk.Scrollbar(var_select)
                s.grid(row=r+1,column=c+1,sticky='ns')
                varlist=['All']+var_list
                listbox=tk.Listbox(var_select, selectmode="multiple", exportselection=0)
                for i,j in zip(range(len(varlist)),varlist):
                    listbox.insert(i,str(j))
                listbox.grid(row=r+1,column=c,sticky='nsew')
                s['command'] = listbox.yview
                listbox['yscrollcommand'] = s.set
                listbox.config(width="0")
            window.withdraw()
            var_select = tk.Toplevel()
            var_select.protocol("WM_DELETE_WINDOW", on_closing)
            var_select.grid_columnconfigure(0,weight=1)
            var_select.grid_columnconfigure(1,weight=0)
            var_select.grid_columnconfigure(2,weight=1)
            var_select.grid_columnconfigure(3,weight=0)
            var_select.grid_columnconfigure(4,weight=1)
            var_select.grid_columnconfigure(5,weight=0)
            var_select.grid_columnconfigure(6,weight=1)
            var_select.grid_columnconfigure(7,weight=0)
            var_select.grid_rowconfigure(0,weight=1)
            var_select.grid_rowconfigure(1,weight=1)
            var_select.grid_rowconfigure(2,weight=1)
            var_select.grid_rowconfigure(3,weight=0)
            var_select.grid_rowconfigure(4,weight=0)
            var_select.grid_rowconfigure(5,weight=0)
            var_select.labelt = tk.Label(var_select, text="National:", anchor="w", font="Arial 12 bold")
            var_select.labelt2 = tk.Label(var_select, text="State:", anchor="w", font="Arial 12 bold")
            var_select.s = tk.Scrollbar(window)
            var_select.labelt.grid(row=0,column=0,sticky='nsew')
            var_select.labelt2.grid(row=5,column=0,sticky='nsew')
            var_select.s.grid(row=2,column=1,sticky='ns')
            labelcbp = tk.Label(var_select, text="var1:", anchor="w",font="Arial 10 bold")
            labelbed = tk.Label(var_select, text="var2:", anchor="w",font="Arial 10 bold")
            labelbds = tk.Label(var_select, text="var3:", anchor="w",font="Arial 10 bold")
            #labelbits = tk.Label(var_select, text="var4:", anchor="w",font="Arial 10 bold")
            
            labelcbp.grid(row=1,column=0)
            labelbed.grid(row=1,column=2)
            labelbds.grid(row=1,column=4)
            #labelbits.grid(row=1,column=6)
            #CBP,BDS,BITS,BED
        #fill in variable cbp list box
            svCBP = tk.Scrollbar(var_select)
            svCBP.grid(row=2,column=1,sticky='ns')
            cbpvar=['All'] + fvariable1
            list_boxcbp = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(cbpvar)),cbpvar):
                list_boxcbp.insert(i, str(j))
            list_boxcbp.grid(row=2,column=0,sticky='nsew')
            svCBP['command'] = list_boxcbp.yview
            list_boxcbp['yscrollcommand'] = svCBP.set
            list_boxcbp.config(width="0")
        #fill in variable bed list box
            svbed = tk.Scrollbar(var_select)
            svbed.grid(row=2,column=3,sticky='ns')
            bedvar=['All'] + fvariable1
            list_boxbed = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bedvar)),bedvar):
                list_boxbed.insert(i, str(j))
            list_boxbed.grid(row=2,column=2,sticky='nsew')
            svbed['command'] = list_boxbed.yview
            list_boxbed['yscrollcommand'] = svbed.set
            list_boxbed.config(width="0")

            create_listbox("Var3:",1,5,fvariable1)
#        #fill in variable bds list box
#            svbds = tk.Scrollbar(var_select)
#            svbds.grid(row=2,column=5,sticky='ns')
#            bdsvar=['All'] + fvariable1
#            list_boxbds = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
#            for i,j in zip(range(len(bdsvar)),bdsvar):
#                list_boxbds.insert(i, str(j))
#            list_boxbds.grid(row=2,column=4,sticky='nsew')
#            svbds['command'] = list_boxbds.yview
#            list_boxbds['yscrollcommand'] = svbds.set
#            list_boxbds.config(width="0")
            
            create_listbox("Var4:",1,6,fvariable1)
#        #fill in variable bits list box
#            svbits = tk.Scrollbar(var_select)
#            svbits.grid(row=2,column=7,sticky='ns')
#            bitsvar=['All'] + fvariable1
#            list_boxbits = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
#            for i,j in zip(range(len(bitsvar)),bitsvar):
#                list_boxbits.insert(i, str(j))
#            list_boxbits.grid(row=2,column=6,sticky='nsew')
#            svbits['command'] = list_boxbits.yview
#            list_boxbits['yscrollcommand'] = svbits.set
#            list_boxbits.config(width="0")
            
            labelcbps2 = tk.Label(var_select, text="var1:", anchor="w",font="Arial 10 bold")
            labelbeds2 = tk.Label(var_select, text="var2:", anchor="w",font="Arial 10 bold")
            labelbdss2 = tk.Label(var_select, text="var3:", anchor="w",font="Arial 10 bold")
            labelbitss2 = tk.Label(var_select, text="var4:", anchor="w",font="Arial 10 bold")
            
            labelcbps2.grid(row=3,column=0)
            labelbeds2.grid(row=3,column=2)
            labelbdss2.grid(row=3,column=4)
            labelbitss2.grid(row=3,column=6)
            

            ###row2###
        #fill in variable cbp list box
            svCBP2 = tk.Scrollbar(var_select)
            svCBP2.grid(row=4,column=1,sticky='ns')
            cbpvar2=['All'] + fvariable1
            list_boxcbp2 = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(cbpvar2)),cbpvar2):
                list_boxcbp2.insert(i, str(j))
            list_boxcbp2.grid(row=4,column=0,sticky='nsew')
            svCBP2['command'] = list_boxcbp2.yview
            list_boxcbp2['yscrollcommand'] = svCBP2.set
            list_boxcbp2.config(width="0")
        #fill in variable bed list box
            svbed2 = tk.Scrollbar(var_select)
            svbed2.grid(row=4,column=3,sticky='ns')
            bedvar2=['All'] + fvariable1
            list_boxbed2 = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bedvar2)),bedvar2):
                list_boxbed2.insert(i, str(j))
            list_boxbed2.grid(row=4,column=2,sticky='nsew')
            svbed2['command'] = list_boxbed2.yview
            list_boxbed2['yscrollcommand'] = svbed2.set
            list_boxbed2.config(width="0")
        #fill in variable bds list box
            svbds2 = tk.Scrollbar(var_select)
            svbds2.grid(row=4,column=5,sticky='ns')
            bdsvar2=['All'] + fvariable1
            list_boxbds2 = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bdsvar2)),bdsvar2):
                list_boxbds2.insert(i, str(j))
            list_boxbds2.grid(row=4,column=4,sticky='nsew')
            svbds2['command'] = list_boxbds2.yview
            list_boxbds2['yscrollcommand'] = svbds2.set
            list_boxbds2.config(width="0")
        #fill in variable bits list box
            svbits2 = tk.Scrollbar(var_select)
            svbits2.grid(row=4,column=7,sticky='ns')
            bitsvar2=['All'] + fvariable1
            list_boxbits2 = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bitsvar2)),bitsvar2):
                list_boxbits2.insert(i, str(j))
            list_boxbits2.grid(row=4,column=6,sticky='nsew')
            svbits2['command'] = list_boxbits2.yview
            list_boxbits2['yscrollcommand'] = svbits2.set
            list_boxbits2.config(width="0")
            
            
            labelcbps = tk.Label(var_select, text="var1:", anchor="w",font="Arial 10 bold")
            labelbeds = tk.Label(var_select, text="var2:", anchor="w",font="Arial 10 bold")
            labelbdss = tk.Label(var_select, text="var3:", anchor="w",font="Arial 10 bold")
            labelbitss = tk.Label(var_select, text="var4:", anchor="w",font="Arial 10 bold")
            
            labelcbps.grid(row=6,column=0)
            labelbeds.grid(row=6,column=2)
            labelbdss.grid(row=6,column=4)
            labelbitss.grid(row=6,column=6)
            
            
            ####state level fill in#######
        #fill in variable cbp list box
            svCBPs = tk.Scrollbar(var_select)
            svCBPs.grid(row=7,column=1,sticky='ns')
            cbpvars=['All'] + fvariable1
            list_boxcbps = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(cbpvars)),cbpvars):
                list_boxcbps.insert(i, str(j))
            list_boxcbps.grid(row=7,column=0,sticky='nsew')
            svCBPs['command'] = list_boxcbps.yview
            list_boxcbps['yscrollcommand'] = svCBPs.set
            list_boxcbps.config(width="0")
        #fill in variable bed list box
            svbeds = tk.Scrollbar(var_select)
            svbeds.grid(row=7,column=3,sticky='ns')
            bedvars=['All'] + fvariable1
            list_boxbeds = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bedvars)),bedvars):
                list_boxbeds.insert(i, str(j))
            list_boxbeds.grid(row=7,column=2,sticky='nsew')
            svbeds['command'] = list_boxbeds.yview
            list_boxbeds['yscrollcommand'] = svbeds.set
            list_boxbeds.config(width="0")
        #fill in variable bds list box
            svbdss = tk.Scrollbar(var_select)
            svbdss.grid(row=7,column=5,sticky='ns')
            bdsvars=['All'] + fvariable1
            list_boxbdss = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bdsvars)),bdsvars):
                list_boxbdss.insert(i, str(j))
            list_boxbdss.grid(row=7,column=4,sticky='nsew')
            svbdss['command'] = list_boxbdss.yview
            list_boxbdss['yscrollcommand'] = svbdss.set
            list_boxbdss.config(width="0")
        #fill in variable bits list box
            svbitss = tk.Scrollbar(var_select)
            svbitss.grid(row=7,column=7,sticky='ns')
            bitsvars=['All'] + fvariable1
            list_boxbitss = tk.Listbox(var_select, selectmode="multiple", exportselection=0)
            for i,j in zip(range(len(bitsvars)),bitsvars):
                list_boxbitss.insert(i, str(j))
            list_boxbitss.grid(row=7,column=6,sticky='nsew')
            svbitss['command'] = list_boxbitss.yview
            list_boxbitss['yscrollcommand'] = svbitss.set
            list_boxbitss.config(width="0")
            
            buttona = tk.Button(var_select, text = "Submit", command = close_var)
            buttona.grid(row=8,column=0, columnspan=3)
            buttonr = tk.Button(var_select, text = "Restart", command = restart)
            buttonr.grid(row=8,column=4, columnspan=3)
            
        self.window=window
        qaGUI.len_max=0
        qaGUI.vdd =tk.StringVar()
        if qaGUI.vdd.get()=="":
            qaGUI.dd = args.datadirectory
        qaGUI.vdd.set(qaGUI.dd)
        qaGUI.vod =tk.StringVar()
        if qaGUI.vod.get()=="":
            qaGUI.od = args.outdirectory
        qaGUI.vod.set(qaGUI.od)
        var_window()
#        window.grid_columnconfigure(0,weight=1)
#        window.grid_columnconfigure(1,weight=0)
#        window.grid_rowconfigure(0,weight=1)
#        window.grid_rowconfigure(1,weight=1)
#        window.grid_rowconfigure(2,weight=1)
#        window.grid_rowconfigure(3,weight=0)
#        window.grid_rowconfigure(4,weight=0)
#        window.grid_rowconfigure(5,weight=0)
#        self.labelt = tk.Label(window, text="Select Tables:", anchor="w", font="Arial 12 bold")
#        self.s = tk.Scrollbar(window)
#        self.labelt.grid(row=0,column=0,sticky='nsew')
#        self.s.grid(row=2,column=1,sticky='ns')
#        fill_list()
#      
#        self.frame = tk.Frame(window)
#        self.frame.grid(row=3,column=0)
#        qaGUI.e = tk.Entry(window, width=self.len_max)
#        self.e.grid(row=1,column=0, sticky='nsew')
#        self.button1 = tk.Button(self.frame, text = "Edit Data Folder", command = lambda:edit_folder(self.window))
#        self.button1.grid(row=4,column=0)
#        self.button = tk.Button(self.frame, text = "Next", command = var_window)
#        self.button.grid(row=5,column=0)
 
standard_table_list = []    

#select bds tables
def table_selection():
    selected_tables = qaGUI.selected_tables
    if selected_tables == 'All':
        selected_tables = standard_table_list
    selected_tables_c = table_clean(selected_tables)
    return selected_tables_c

#make sure the tables match needed level to match high level
def table_clean(tables):
    
    return c_selected_tables

#select bds variables
def variable_selection():
    variable_list=[]
    variable_list.extend(qaGUI.selected_variablesbed)
    variable_list.extend(qaGUI.selected_variablesbds)
    variable_list.extend(qaGUI.selected_variablescbp)
    variable_list.extend(qaGUI.selected_variablesbits)
    return variable_list

#match bds variables to high level tables
def variable_cross():
    return hd_variables

#plot comparison
def plot_maker():
    x

#initialization
if __name__=="__main__":
    #arguments for run from command line
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
    #dictionary for sorting the most likely tables
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
    
   #list of most likely variables
#    fvariable1=["Firms","Estabs","Emp","Denom","Estabs_Entry","Estabs_Exit","Job_Creation","Job_Creation_Births","Job_Creation_Continuers","Job_Destruction","Job_Destruction_Deaths","Job_Destruction_Continuers","Net_Job_Creation","Firmdeath_Firms","Firmdeath_Estabs","Firmdeath_Emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]
#    fvariable2=["firms","estabs","emp","denom","estabs_entry","estabs_exit","job_creation","job_creation_births","job_creation_continuers","job_destruction","job_destruction_deaths","job_destruction_continuers","net_job_creation","firmdeath_firms","firmdeath_estabs","firmdeath_emp","Estabs_Continuers_Expanding","Estabs_Continuers_Contracting"]
#    
    fvariable1 = ["Firms","Estabs","Job Creation","Job Destruction"]

#run Gui
    master = tk.Tk()
    window = qaGUI(master)
 
    def on_closing():
        raise SystemExit
    
    master.protocol("WM_DELETE_WINDOW", on_closing)
    
    tk.mainloop()


    try: window.od
    except AttributeError: window.od = None
    if window.od != None:
        if str(window.od) !="":
           odirectory  = str(window.od)    
    if not odirectory.endswith("/"):
        odirectory= odirectory + "/"
        
    try: window.dd
    except AttributeError: window.dd = None
    if window.dd != None:
        if str(window.dd) !="":
           ddirectory  = str(window.dd)    
    if not ddirectory.endswith("/"):
        ddirectory= ddirectory + "/"


#    c_tables = table_selection(qaGUI.selected_tables)
#    for f in c_tables:
#        data=pd.read_csv(ddirectory+f+".csv")
#        datahd=hd
#        for j in variable_selection():
#            plot_maker(data,j,hddata)
            
    print(odirectory)
    print(variable_selection())
    print(qaGUI.selected_tables)