# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 10:00:41 2018

@author: rl7276c
"""

import os
import pandas as pd
import time
import numpy as np

path = "M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets\\completed"
cleanpath = "M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets\\\county_sub_files_clean"

nlist = [11, 21, 22, 23, 31, 32, 33, 42, 44, 45, 48, 49, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 81, 99]
n1list = [11, 21, 22, 23, 42, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 81, 99]
n2list=[31]
n3list=[42]
n4list=[44]
n5list=[48]

filelist=os.listdir(path)
#filelist.remove(filelist[0])
filelists=filelist

cbp_county=pd.DataFrame(columns=['cty_naics', 	'e_range', 	'emp', 	'ap', 	'est', 	'fipstate', 	'fipscty', 	'fipsstcty', 	'stctyid', 	'emp_nf', 	'naics', 	'naics_len', 	'naics2', 	'naics3', 	'naics4', 	'naics5', 	'clean_flag'	])
for filename in filelists:
    df = pd.read_csv(path+"/"+filename)
    df=df[	['cty_naics', 	'e_range', 	'emp', 	'ap', 	'est', 	'fipstate', 	'fipscty', 	'fipsstcty', 	'stctyid', 	'emp_nf', 	'naics', 	'naics_len', 	'naics2', 	'naics3', 	'naics4', 	'naics5', 	'clean_flag'	]]
    cbp_county=cbp_county.append(df)
    

#f=[len(df2['stctyid'].unique())]
#len(f)


cbp_county['clean_flag_2']=0
cbp_county.loc[(cbp_county['emp'].isna()), 'clean_flag_2']=1
cbp_county.loc[(cbp_county['ap'].isna()), 'clean_flag_2']=1
cbp_county.loc[(cbp_county['emp']<0), 'clean_flag_2']=1
cbp_county.loc[(cbp_county['ap']<0), 'clean_flag_2']=1
cbp_county.loc[(cbp_county['emp']==0)&(cbp_county['e_range']>10), 'clean_flag_2']=1
cbp_county.loc[(cbp_county['ap']==0)&(cbp_county['emp']>0), 'clean_flag_2']=1

df1=cbp_county[['stctyid','clean_flag_2']].groupby('stctyid').sum().reset_index()
df1.loc[df1['clean_flag_2']>1,'clean_flag']=1
df1=df1[df1['clean_flag_2']==1]

df2= cbp_county.loc[cbp_county['stctyid'].isin(df1['stctyid'])]
df3= cbp_county.loc[~cbp_county['stctyid'].isin(df1['stctyid'])]


df2.to_csv('M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets\\to_fix.csv')

df4=pd.read_csv(cleanpath+"/fixed.csv")

dff=df3.append(df4)
dff.to_csv(path+"/cbp_erange_cty.csv")

###you cheated here will need a real fix
df3.loc[df3['ap']<0,'ap']=0
df3.loc[df3['emp']<0,'emp']=0

sum(dff['emp']<0)
######################################################################################
list(df2)
d2=pd.read_csv('M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets\\to_fix_emp_fix.csv')
df2.loc[(df2['naics']!='Total')&(df2['e_range'].notna()),'emp']=0
#df2.loc[df2['emp'].isna(),'emp']=0
df2.loc[df2['ap'].isna(),'ap']=0
df2.loc[(df2['emp']==0)&df2['e_range'].isna(),'e_range']=0
df2.loc[df2['e_range']<0,'e_range']=0
df2.loc[df2['e_range'].notna(),'ap']=0   
df2.sort_values(['stctyid','naics_len'], ascending=False)
df2['cty_naics']=df2['stctyid'].map(str)+'-'+df2['naics'].map(str)
#lister=df2.loc[(df2['emp']>0)&(df2['naics_len']>2),'cty_naics'].values
#for i in reversed(lister) :
#    code=i[:-1]
#    cu=df2.loc[df2['cty_naics']==i,'emp'].item()
#    try:
#        up=df2.loc[df2['cty_naics']==code,'emp'].item()
#    except:
#        up=0
#    if up < cu:
#        org=df2.loc[df2['cty_naics']==code,'emp']
#        df2.loc[df2['cty_naics']==code,'emp']=org+(df2.loc[df2['cty_naics']==i, 'emp'].item())    
cbp_erange=df2
cbp_erange.set_index('cty_naics',inplace=True)
cutoff=cbp_erange['stctyid'].min()
cutofft=cbp_erange['stctyid'].max()
vcount=cbp_erange["stctyid"].value_counts().count()+1

naics_list5=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:4])
naics_list6=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:5])

state_range=cbp_erange['stctyid'].unique()
#list(range(cutoff,cutofft))

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
#total_time4=t3-t0
#print(total_time4)
 #Export filled data
cbp_erange.to_csv(cleanpath+"/try4_"+filename)





  

