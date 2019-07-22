# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 20:36:49 2018

@author: rl7276c
"""

import os
import pandas as pd
import time
import numpy as np

path = "M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets\\county_sub_files"
cleanpath = "M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets\\\county_sub_files_clean"

nlist = [11, 21, 22, 23, 31, 32, 33, 42, 44, 45, 48, 49, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 81, 99]
n1list = [11, 21, 22, 23, 42, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 81, 99]
n2list=[31]
n3list=[42]
n4list=[44]
n5list=[48]

filelist=os.listdir(path)
#filelist.remove(filelist[0])
filelists=[filelist[4]]


for filename in filelists:
    df = pd.read_csv(path+"/"+filename)
    cbp_erange=df
    cbp_erange.set_index('cty_naics',inplace=True)
    cutoff=cbp_erange['stctyid'].min()
    cutofft=cbp_erange['stctyid'].max()
    vcount=cbp_erange["stctyid"].value_counts().count()+1
    
    naics_list5=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:4])
    naics_list6=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:5])
    
    state_range=df['stctyid'].unique()
    #list(range(cutoff,cutofft))
    
    t0=time.time()
#    
#    cbp_erange['naics2'] = cbp_erange['naics'].str[:2]
#    cbp_erange['naics3'] = cbp_erange['naics'].str[:3]
#    cbp_erange['naics4'] = cbp_erange['naics'].str[:4]
#    cbp_erange['naics5'] = cbp_erange['naics'].str[:5]
#    
#    cbp_erange.loc[cbp_erange['naics2'].isin(['32','33']),'naics2'] = '31'
#    cbp_erange.loc[cbp_erange['naics2'].isin(['43']),'naics2'] = '42'
#    cbp_erange.loc[cbp_erange['naics2'].isin(['45']),'naics2'] = '44'
#    cbp_erange.loc[cbp_erange['naics2'].isin(['49']),'naics2'] = '48'
       

    
    t21 = time.time()
    print(t21-t0)
    
    #Two digit emp
    State_var = 1 
    for State_var in state_range:
        NAICS_var = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0    
        for NAICS_var in nlist:
            if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
                if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']):
                    count1_string = str(State_var)+'-'+str(NAICS_var)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']
                    print(flagsum)
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
        if count == 1:
            if cbp_erange.loc[count1_string,'emp']==0:
                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_var = 0
            NAICS_rem = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
            for NAICS_var in nlist:
                if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']):
                        new = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
                        if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'].item():
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
    
    t22 = time.time()
    print(t22-t21)
  

    
    t31 = time.time()
    print(t31-t22)
    
    #Three digit emp
    State_var = 0 
    for State_var in state_range:
        #NAICS 11-23, 44, 51+
        for NAICS_var in n1list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new >  cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 
    
      
        #NAICS 31-33
        for NAICS_var in n2list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index:   
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
                if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index:  
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
                if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
    
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index: 
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
                    if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index: 
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new >cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
      
                    if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new >cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
        #NAICS 44-45
        for NAICS_var in n4list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index:  
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
                if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index: 
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                    if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new> cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem   
    
        #NAICS 48-49
        for NAICS_var in n5list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
                if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                    if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']):
                            new = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
        
    t32 = time.time()
    print(t32-t31)
    
    
        
    
    t41 = time.time()
    print(t41-t32)
    
    #Four digit emp
    State_var = 0 
    for State_var in state_range:
        for i in nlist:
            for d in range(10):
                NAICS_var=str(i)+str(d)   
                NAICS_rest_sum = 0
                count = 0
                count1_string = ""
                flagsum = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                if count == 1:
                    if cbp_erange.loc[count1_string,'emp']==0:
                        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                if count > 1:
                    NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                    NAICS_var_2 = 0
                    for NAICS_var_2 in range(10):
                        if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                            if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                                new = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                                if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'].item():
                                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
    t42 = time.time()
    print(t42-t41)
    
         
    
    t51 = time.time()
    print(t51-t42)
    
    #Five digit emp
    
    for State_var in state_range:
        for i in nlist:
            for d in range(11,100):
                NAICS_var=str(i)+str(d)
                NAICS_rest_sum = 0
                count = 0
                count1_string = ""
                flagsum = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                if count == 1:
                    if cbp_erange.loc[count1_string,'emp']==0:
                        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                if count > 1:
                    NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                    for NAICS_var_2 in range(10):
                        if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                            if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                                new = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 
                                if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'].item():
                                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 
    
    
    t52 = time.time()
    print(t52-t51)
    #Six digit emp
     
    for State_var in state_range:
        for NAICS_var in naics_list6:   
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                    if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                        if pd.notna(cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']):
                            new= cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
    
    t61 = time.time()
    print(t61-t52)
    
    t1=time.time()
    total_time=t1-t0
    print('emp took '+str(total_time))  
    
    #Ap variable
    
    #Two digit ap
    State_var = 1  
    for State_var in state_range:
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0    
        for NAICS_var in nlist:
            if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap']
        if count == 1:
            if cbp_erange.loc[count1_string,'emp']==0:
                cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-Total','ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_var = 0
            NAICS_rem = cbp_erange.loc[str(State_var)+'-Total','ap'] - NAICS_rest_sum
            for NAICS_var in nlist:
                if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] / flagsum * NAICS_rem
        State_var = State_var + 1
    
    #Three digit ap
    
    for State_var in state_range:
        #NAICS 11-23
        for NAICS_var in n1list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                 if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
        #NAICS 31-33
        for NAICS_var in n2list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap']
                if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap']
                if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:   
                    if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                    if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index:
                        if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                    if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                        if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
       
        #NAICS 44-45
        for NAICS_var in n4list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index:   
                    if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap']
                if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:   
                    if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index:  
                        if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                    if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
      
        #NAICS 48-49
        for NAICS_var in n5list:
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap']
                if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap']
    
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                    if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
        State_var = State_var + 1
    
    #Four digit ap
     

    for State_var in state_range:
        for i in nlist:
            for d in range(10):
                NAICS_var=str(i)+str(d) 
                NAICS_rest_sum = 0
                count = 0
                count1_string = ""
                flagsum = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
                if count == 1:
                    if cbp_erange.loc[count1_string,'emp']==0:
                        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                if count > 1:
                    NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                    NAICS_var_2 = 0
                    for NAICS_var_2 in range(10):
                        if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                                cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
    
    
    #Five digit ap
    for State_var in state_range:
        for NAICS_var in naics_list5:  
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem   
    
    
    #Six digit ap
    for State_var in state_range:
        for NAICS_var in naics_list6:  
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            if count == 1:
                if cbp_erange.loc[count1_string,'emp']==0:
                    cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem 
    
    t3=time.time()
    total_time3=t3-t1
    total_time4=t3-t0
    print(total_time3)
    print(total_time4)
     #Export filled data
    cbp_erange.to_csv(cleanpath+"/try3_"+filename)



