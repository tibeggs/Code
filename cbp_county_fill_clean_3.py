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
filelists=[filelist[0]]


for filename in filelists:
    df = pd.read_csv(path+"/"+filename)
    df['clean_flag']=0
    df.loc[(df['emp'].isna()), 'clean_flag']=1
    df.loc[(df['emp']<0), 'clean_flag']=1
    df1=df[['stctyid','clean_flag']].groupby('stctyid').sum().reset_index()
    df1.loc[df1['clean_flag']>1,'clean_flag']=1
    df1=df1[df1['clean_flag']==1]
    df2= df.loc[df['stctyid'].isin(df1['stctyid'])]
    df2.loc[(df2['naics']!='Total')&(df2['e_range'].notna()),'emp']=0
    df2.loc[df2['emp'].isna(),'emp']=0
    df2.loc[(df2['emp']==0)&df2['e_range'].isna(),'e_range']=0
    df2.loc[df2['e_range']<0,'e_range']=0   
    df2.sort_values(['stctyid','naics_len'], ascending=False)
    for i in df2.loc[(df2['emp']>0)&(df2['naics_len']>2),'cty_naics']:
        code=i[:-1]
        cu=df2.loc[df2['cty_naics']==i,'emp'].item()
        try:
            up=df2.loc[df2['cty_naics']==code,'emp'].item()
        except:
            up=0
        if up < cu:
            org=df2.loc[df2['cty_naics']==code,'emp']
            df2.loc[df2['cty_naics']==code,'emp']=org+(df2.loc[df2['cty_naics']==i, 'emp'].item())    
    df3= df.loc[~df['stctyid'].isin(df1['stctyid'])]
    df3.to_csv(cleanpath+"/sucess_"+filename)
    cbp_erange=df2
    cbp_erange.set_index('cty_naics',inplace=True)
    cutoff=cbp_erange['stctyid'].min()
    cutofft=cbp_erange['stctyid'].max()
    vcount=cbp_erange["stctyid"].value_counts().count()+1
    
    naics_list5=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:4])
    naics_list6=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:5])
    
    state_range=df1['stctyid']
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
       
    #need to add measure for above sum being 0
    for naics_code in cbp_erange[cbp_erange['naics_len']==2].index:
        if (cbp_erange.loc[naics_code,'naics2']!='99')&(cbp_erange.loc[naics_code,'naics2']!='To'):
            dfl=cbp_erange[['stctyid','naics_len','emp','e_range']].groupby(['stctyid','naics_len']).sum().reset_index()
            dfl.columns = ['stctyid','naics_len','emp_sum','erange_sum']
            dfl1=cbp_erange[['stctyid','naics2','naics_len','emp','e_range']].groupby(['stctyid','naics2','naics_len']).sum().reset_index()
            dfl1.columns = ['stctyid','naics2','naics_len','emp_sum','erange_sum']
            if cbp_erange.loc[naics_code,'emp']==0:
                a = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl['naics_len']==2), 'emp_sum'].item()
                b = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl['naics_len']==1), 'emp_sum'].item()
                dif = b-a
                c = cbp_erange.loc[naics_code,'e_range']
                d = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl['naics_len']==2), 'erange_sum'].item()
                per = c/d
                e = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'emp_sum'].item()
                f = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'erange_sum'].item()
                try:
                    g = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+2)), 'emp_sum'].item()
                except:
                    g = 0
                if (dif!=0)&((per*dif)-e>0)&((per*dif)-e<g):
                    e=e+(g-((per*dif)-e))
                try:
                    h = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+3)), 'emp_sum'].item()
                except:
                    h = 0
                if (dif!=0)&((per*dif)-e>0)&((per*dif)-e<h):
                    e=e+(h-((per*dif)-e))
                try:
                    i = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+4)), 'emp_sum'].item()
                except:
                    i = 0
                if (dif!=0)&((per*dif)-e>0)&((per*dif)-e<i):
                    e=e+(g-((per*dif)-i))
                if (per*dif <= e)&(dif!=0):
                    if dif == e:
                        cbp_erange.loc[(naics_code),'e_range'] = d
                    else:
                        x = (e*d/dif)/(1-e/dif)
                        new_range = f/4 + x
                        cbp_erange.loc[(naics_code),'e_range'] = new_range   
                    
                dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))]
    
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
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'])!=0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_var = 0
            NAICS_rem = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
            for NAICS_var in nlist:
                if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'])!=0):
                        new = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
                        if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'].item():
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
    
    t22 = time.time()
    print(t22-t21)
  
    for naics_code in cbp_erange[cbp_erange['naics_len']==3].index:
        dfl=cbp_erange[['stctyid','naics2','naics_len','emp','e_range']].groupby(['stctyid','naics2','naics_len']).sum().reset_index()
        dfl.columns = ['stctyid','naics2','naics_len','emp_sum','erange_sum']
        dfl1=cbp_erange[['stctyid','naics3','naics_len','emp','e_range']].groupby(['stctyid','naics3','naics_len']).sum().reset_index()
        dfl1.columns = ['stctyid','naics3','naics_len','emp_sum','erange_sum']
        if cbp_erange.loc[naics_code,'emp']==0:
          #  dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics2']==(cbp_erange.loc[(naics_code),'naics2']))]
            a = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics2']==(cbp_erange.loc[(naics_code),'naics2'])) & (dfl['naics_len']==3), 'emp_sum'].item()
            b = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics2']==(cbp_erange.loc[(naics_code),'naics2']))& (dfl['naics_len']==2), 'emp_sum'].item()
            dif = b-a
            c = cbp_erange.loc[naics_code,'e_range']
            d = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl['naics_len']==3), 'erange_sum'].item()
            per = c/d
            e = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics3']==(cbp_erange.loc[(naics_code),'naics3']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'emp_sum'].item()
            f = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics3']==(cbp_erange.loc[(naics_code),'naics3']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'erange_sum'].item()
            try:
                g = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics3']==(cbp_erange.loc[(naics_code),'naics3']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+2)), 'emp_sum'].item()
            except:
                g = 0
            if (dif!=0)&((per*dif)-e>0)&((per*dif)-e<g):
                e=e+(g-((per*dif)-e))
            try:
                h = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+3)), 'emp_sum'].item()
            except:
                h = 0
            if (dif!=0)&((per*dif)-e>0)&((per*dif)-e<h):
                e=e+(h-((per*dif)-e))
            if (per*dif <= e)&(dif!=0):
                if dif == e:
                    cbp_erange.loc[(naics_code),'e_range'] = d  
                else:
                    x = (e*d/dif)/(1-e/dif)
                    new_range = f/4 + x
                    if new_range > 0:
                        cbp_erange.loc[(naics_code),'e_range'] = new_range  
                        
    
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
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            if count == 1:
                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
                if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
                if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
    
            if count == 1:
                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'])!=0):
                            new = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
                    if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'])!=0):
                            new = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new >cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
      
                    if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                        if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'])!=0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
                if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
            if count == 1:
                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'])!=0):
                            new = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                    if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
                        if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'])!=0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                        count = count + 1                    
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
                if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
            if count == 1:
                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
                        if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'])!=0):
                            new = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                    if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'])!=0):
                            new = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'].item():
                                cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
        
    t32 = time.time()
    print(t32-t31)
    
    
    for naics_code in cbp_erange[cbp_erange['naics_len']==4].index:
        dfl=cbp_erange[['stctyid','naics3','naics_len','emp','e_range']].groupby(['stctyid','naics3','naics_len']).sum().reset_index()
        dfl.columns = ['stctyid','naics3','naics_len','emp_sum','erange_sum']
        dfl1=cbp_erange[['stctyid','naics4','naics_len','emp','e_range']].groupby(['stctyid','naics4','naics_len']).sum().reset_index()
        dfl1.columns = ['stctyid','naics4','naics_len','emp_sum','erange_sum']
        if cbp_erange.loc[naics_code,'emp']==0:
            a = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics3']==(cbp_erange.loc[(naics_code),'naics3'])) & (dfl['naics_len']==4), 'emp_sum'].item()
            b = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics3']==(cbp_erange.loc[(naics_code),'naics3']))& (dfl['naics_len']==3), 'emp_sum'].item()
            dif = b-a
            c = cbp_erange.loc[naics_code,'e_range']
            d = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl['naics3']==(cbp_erange.loc[(naics_code),'naics3']))&(dfl['naics_len']==4), 'erange_sum'].item()
            per = c/d
            e = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics4']==(cbp_erange.loc[(naics_code),'naics4']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'emp_sum'].item()
            f = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics4']==(cbp_erange.loc[(naics_code),'naics4']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'erange_sum'].item()
            try:
                g = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics4']==(cbp_erange.loc[(naics_code),'naics4']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+2)), 'emp_sum'].item()
            except:
                g=0
            if (dif!=0)&((per*dif)-e>0)&((per*dif)-e<g):
                e=e+(g-((per*dif)-e))
            if (per*dif <= e)&(dif!=0):
                if dif == e:
                    cbp_erange.loc[(naics_code),'e_range'] = d  
                else:
                    x = (e*d/dif)/(1-e/dif)
                    new_range = f/4 + x
                    if new_range > 0:
                        cbp_erange.loc[(naics_code),'e_range'] = new_range            
    
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
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                if count == 1:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                if count > 1:
                    NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                    NAICS_var_2 = 0
                    for NAICS_var_2 in range(10):
                        if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
                                new = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                                if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'].item()
                                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
    t42 = time.time()
    print(t42-t41)
    
    for naics_code in cbp_erange[cbp_erange['naics_len']==5].index:
        dfl=cbp_erange[['stctyid','naics4','naics_len','emp','e_range']].groupby(['stctyid','naics4','naics_len']).sum().reset_index()
        dfl.columns = ['stctyid','naics4','naics_len','emp_sum','erange_sum']
        dfl1=cbp_erange[['stctyid','naics5','naics_len','emp','e_range']].groupby(['stctyid','naics5','naics_len']).sum().reset_index()
        dfl1.columns = ['stctyid','naics5','naics_len','emp_sum','erange_sum']
        if cbp_erange.loc[naics_code,'emp']==0:
            a = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics4']==(cbp_erange.loc[(naics_code),'naics4'])) & (dfl['naics_len']==5), 'emp_sum'].item()
            b = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl['naics4']==(cbp_erange.loc[(naics_code),'naics4']))& (dfl['naics_len']==4), 'emp_sum'].item()
            dif = b-a
            c = cbp_erange.loc[naics_code,'e_range']
            d = dfl.loc[(dfl['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl['naics4']==(cbp_erange.loc[(naics_code),'naics4']))&(dfl['naics_len']==5), 'erange_sum'].item()
            per = c/d
            e = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics5']==(cbp_erange.loc[(naics_code),'naics5']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'emp_sum'].item()
            f = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics5']==(cbp_erange.loc[(naics_code),'naics5']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+1)), 'erange_sum'].item()
            if (per*dif <= e)&(dif!=0):
                if dif == e:
                    cbp_erange.loc[(naics_code),'e_range'] = d  
                else:
                    x = (e*d/dif)/(1-e/dif)
                    new_range = f/4 + x
                    if new_range > 0:
                        cbp_erange.loc[(naics_code),'e_range'] = new_range               
    
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
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
                            count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                            count = count + 1
                            flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                        else:
                            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                if count == 1:
                    cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                if count > 1:
                    NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                    for NAICS_var_2 in range(10):
                        if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                        count = count + 1
                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                    else:
                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            if count == 1:
                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            if count > 1:
                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
                NAICS_var_2 = 0
                for NAICS_var_2 in range(10):
                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'])!=0):
                            new= cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                            if new > cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'].item()
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