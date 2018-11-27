# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:33:13 2018

@author: rl7276c
"""

#Import libraries
import pandas as pd
import time



#Import cbp state data
path = "M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets"
cbp = pd.read_csv(path +"\\cbp12co.csv")
state_totals = pd.read_csv(path+"\\cbp_state_totals.csv")
cbp = cbp[['fipstate','fipscty','naics','empflag','emp','ap','est','emp_nf']]

#Import employment range data and merge with cbp state data
erange = pd.read_csv(path+ '/employment_ranges.csv')
cbp_erange = pd.merge(cbp, erange,how='left',on='empflag')



cbp_erange["fipsstcty"]=cbp_erange["fipstate"].astype(str)+"-"+cbp_erange["fipscty"].astype(str)
cbp_erange["stctyid"]=cbp_erange["fipsstcty"].rank(method='dense').astype(int)

cutoff=1

#cbp_erange=cbp_erange[cbp_erange["stctyid"]<=100]

#Clean cbp state data and prepare for filling
cbp_erange['naics'] = cbp_erange['naics'].str.replace('------','Total')

cbp_erange['naics'] = cbp_erange['naics'].str.replace('/','')
cbp_erange['naics'] = cbp_erange['naics'].str.replace('-','')



naics_list5=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:4])
naics_list6=set(cbp_erange['naics'][cbp_erange['naics'].str.len()==6].str[:5])



cbp_erange['cty_naics'] = cbp_erange['stctyid'].map(str) + '-' + cbp_erange['naics'].map(str)
cbp_erange.head()
cbp_erange = cbp_erange[['e_range','emp','ap','est','cty_naics','fipstate','fipscty','fipsstcty','stctyid','emp_nf','naics']]
cbp_erange.set_index('cty_naics',inplace=True)
cbp_erange.head()

#Emp variable

vcount=cbp_erange["stctyid"].value_counts().count()+1

cbp_erange['naics_len'] = cbp_erange['naics'].str.len()


#start timing


for state_var in range(vcount):
    naics_code=str(state_var)+"-Total"
    if naics_code in cbp_erange.index:
        cbp_erange.loc[naics_code,'naics_len'] = 1



nlist = [11, 21, 22, 23, 31, 32, 33, 42, 44, 45, 48, 49, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 81, 99]
n1list = [11, 21, 22, 23, 42, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 81, 99]
n2list=[31]
n3list=[42]
n4list=[44]
n5list=[48]



df1=cbp_erange.loc[(cbp_erange['naics_len']==1)][['fipstate','emp']].groupby('fipstate').sum()
df2=cbp_erange.loc[(cbp_erange['naics_len']==1)][['fipstate','e_range']].groupby('fipstate').sum()
df3=cbp_erange.loc[(cbp_erange['naics_len']==1)][['fipstate','ap']].groupby('fipstate').sum()
df4=cbp_erange.loc[(cbp_erange['naics_len']==1)&(cbp_erange['e_range'].notnull())][['fipstate','emp']].groupby('fipstate').sum()


#does not work if on limited set due to how stctyid works need to be on whole bundle
state_var=1
for state_var in range(vcount):
    naics_code=str(state_var)+"-Total"
    if naics_code in cbp_erange.index:
        dfl=cbp_erange[['stctyid','naics_len','emp','ap','e_range']].groupby(['stctyid','naics_len']).sum().reset_index()
        dfl.columns = ['stctyid','naics_len','emp_sum','ap_sum','erange_sum']
        if (cbp_erange.loc[naics_code,'emp']==0):
            state = cbp_erange.loc[naics_code,'fipstate']
            cbp_erange.loc[naics_code,'emp'] =(state_totals.loc[state_totals['fipstate']==state]['emp'].item()-df1.loc[state].item())*cbp_erange.loc[naics_code,'e_range'] /df2.loc[state].item()
        if (cbp_erange.loc[naics_code,'ap']==0):
            state = cbp_erange.loc[naics_code,'fipstate']
            cbp_erange.loc[naics_code,'ap'] =(state_totals.loc[state_totals['fipstate']==state]['ap'].item()-df3.loc[state].item())*cbp_erange.loc[naics_code,'e_range'] /df2.loc[state].item()

#limit count to 50
cbp_erange = cbp_erange[cbp_erange['stctyid']<=cutoff]
vcount=cbp_erange["stctyid"].value_counts().count()+1

t0=time.time()

cbp_erange['naics2'] = cbp_erange['naics'].str[:2]
cbp_erange['naics3'] = cbp_erange['naics'].str[:3]
cbp_erange['naics4'] = cbp_erange['naics'].str[:4]
cbp_erange['naics5'] = cbp_erange['naics'].str[:5]

cbp_erange.loc[cbp_erange['naics2'].isin(['32','33']),'naics2'] = '31'
cbp_erange.loc[cbp_erange['naics2'].isin(['43']),'naics2'] = '42'
cbp_erange.loc[cbp_erange['naics2'].isin(['45']),'naics2'] = '44'
cbp_erange.loc[cbp_erange['naics2'].isin(['49']),'naics2'] = '48'


#dfl=cbp_erange[['stctyid','naics_len','emp','e_range']].groupby(['stctyid','naics_len']).sum().reset_index()
#dfl.columns = ['stctyid','naics_len','emp_sum','erange_sum']
#    
#dfl1=cbp_erange[['stctyid','naics2','naics_len','emp','e_range']].groupby(['stctyid','naics2','naics_len']).sum().reset_index()
#dfl1.columns = ['stctyid','naics2','naics_len','emp_sum','erange_sum']
#
#dfl2=cbp_erange[['stctyid','naics3','naics_len','emp','e_range']].groupby(['stctyid','naics3','naics_len']).sum().reset_index()
#dfl2.columns = ['stctyid','naics3','naics_len','emp_sum','erange_sum']
#
#dfl3=cbp_erange[['stctyid','naics4','naics_len','emp','e_range']].groupby(['stctyid','naics4','naics_len']).sum().reset_index()
#dfl3.columns = ['stctyid','naics4','naics_len','emp_sum','erange_sum']
#
#dfl4=cbp_erange[['stctyid','naics5','naics_len','emp','e_range']].groupby(['stctyid','naics5','naics_len']).sum().reset_index()
#dfl4.columns = ['stctyid','naics5','naics_len','emp_sum','erange_sum']
#
#dfl1[(dfl1['stctyid']==2)&(dfl1['naics2']=='11')].groupby(['stctyid','naics2']).count()
#dfl1[(dfl1['stctyid']==2)&(dfl1['naics2']=='11')&(dfl1['naics_len']==3)]['emp_sum']
#dfl1[(dfl1['stctyid']==2)&(dfl1['naics2']=='11')&(dfl1['naics_len']==3)]['emp_sum']
#dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))]
#dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))& (dfl1['naics2']=='To')]

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
            if (dif!=0)&((per*dif)-e<g):
                e=e+g
            if (per*dif <= e)&(dif!=0):
                if dif == e:
                    cbp_erange.loc[(naics_code),'e_range'] = d
                else:
                    x = (e*d/dif)/(1-e/dif)
                    new_range = f + x
                    cbp_erange.loc[(naics_code),'e_range'] = new_range   
                
            dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics2']==(cbp_erange.loc[(naics_code),'naics2']))]

#Two digit emp
State_var = 1 
while State_var < vcount:
    NAICS_var = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0    
    for NAICS_var in nlist:
        if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
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
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
    State_var = State_var + 1

for naics_code in cbp_erange[cbp_erange['naics_len']==3].index:
    dfl=cbp_erange[['stctyid','naics2','naics_len','emp','e_range']].groupby(['stctyid','naics2','naics_len']).sum().reset_index()
    dfl.columns = ['stctyid','naics2','naics_len','emp_sum','erange_sum']
    dfl1=cbp_erange[['stctyid','naics3','naics_len','emp','e_range']].groupby(['stctyid','naics3','naics_len']).sum().reset_index()
    dfl1.columns = ['stctyid','naics3','naics_len','emp_sum','erange_sum']
    if cbp_erange.loc[naics_code,'emp']==0:
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
        if (dif!=0)&((per*dif)-e<g):
            e=e+g
        if (per*dif <= e)&(dif!=0):
            if dif == e:
                cbp_erange.loc[(naics_code),'e_range'] = d  
            else:
                x = (e*d/dif)/(1-e/dif)
                new_range = f + x
                if new_range > 0:
                    cbp_erange.loc[(naics_code),'e_range'] = new_range     

#Three digit emp
State_var = 0 
while State_var < vcount:
    #NAICS 11-23, 44, 51+
    for NAICS_var in n1list:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        for NAICS_var_2 in range(10):
            if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 

  
    #NAICS 31-33
    for NAICS_var in n2list:
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        for NAICS_var_2 in range(10):
            if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index:   
                if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
            if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index:  
                if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
            if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem

                if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
  
                if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem

    #NAICS 44-45
    for NAICS_var in n4list:
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        for NAICS_var_2 in range(10):
            if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index:  
                if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
            if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
                if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
                    if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem   

    #NAICS 48-49
    for NAICS_var in n5list:
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        for NAICS_var_2 in range(10):
            if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
                if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
            if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    
    State_var = State_var + 1

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
        if (dif!=0)&((per*dif)-e<g):
            e=e+g
        if (per*dif <= e)&(dif!=0):
            if dif == e:
                cbp_erange.loc[(naics_code),'e_range'] = d  
            else:
                x = (e*d/dif)/(1-e/dif)
                new_range = f + x
                if new_range > 0:
                    cbp_erange.loc[(naics_code),'e_range'] = new_range            

#Four digit emp
State_var = 0 
while State_var < vcount:
    for i in nlist:
        for d in range(10):
            NAICS_var=str(i)+str(d)   
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
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
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    State_var = State_var + 1

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
        try:
            g = dfl1.loc[(dfl1['stctyid']==(cbp_erange.loc[(naics_code),'stctyid']))&(dfl1['naics5']==(cbp_erange.loc[(naics_code),'naics5']))&(dfl1['naics_len']==(cbp_erange.loc[(naics_code),'naics_len']+2)), 'emp_sum'].item()
        except:
            g = 0
        if (dif!=0)&((per*dif)-e<g):
            e=e+g
        if (per*dif <= e)&(dif!=0):
            if dif == e:
                cbp_erange.loc[(naics_code),'e_range'] = d  
            else:
                x = (e*d/dif)/(1-e/dif)
                new_range = f + x
                if new_range > 0:
                    cbp_erange.loc[(naics_code),'e_range'] = new_range               


#Five digit emp
State_var = 0 
while State_var < vcount:
    for i in nlist:
        for d in range(11,100):
            NAICS_var=str(i)+str(d)
            NAICS_rest_sum = 0
            count = 0
            count1_string = ""
            flagsum = 0
            for NAICS_var_2 in range(10):
                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
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
                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 
    State_var = State_var + 1


#Six digit emp
State_var = 0 
while State_var < vcount:
    for NAICS_var in naics_list6:   
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        for NAICS_var_2 in range(10):
            if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
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
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
    State_var = State_var + 1

t1=time.time()
total_time=t1-t0
print(total_time)

#cbp_erange.to_csv(path+"\\outtest.csv")

#
#
##Two digit emp
#
#State_var = 1 
#while State_var < vcount:
#    NAICS_var = 0
#    NAICS_rest_sum = 0
#    count = 0
#    count1_string = ""
#    flagsum = 0    
#    for NAICS_var in nlist:
#        if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
#            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
#                count1_string = str(State_var)+'-'+str(NAICS_var)
#                count = count + 1
#                flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']
#            else:
#                NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
#    if count == 1:
#        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
#    if count > 1:
#        NAICS_var = 0
#        NAICS_rem = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
#        for NAICS_var in nlist:
#            if str(State_var)+"-"+str(NAICS_var) in cbp_erange.index:
#                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
#                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
#    State_var = State_var + 1
#
#
##Three digit emp
#State_var = 0 
#while State_var < vcount:
#    #NAICS 11-23, 44, 51+
#    for NAICS_var in n1list:
#        NAICS_var_2 = 0
#        NAICS_rest_sum = 0
#        count = 0
#        count1_string = ""
#        flagsum = 0
#        for NAICS_var_2 in range(10):
#            if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
#                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
#                        count = count + 1
#                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
#                    else:
#                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
#        if count == 1:
#            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#        if count > 1:
#            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            NAICS_var_2 = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
#                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 
#
#  
#    #NAICS 31-33
#    for NAICS_var in n2list:
#        NAICS_rest_sum = 0
#        count = 0
#        count1_string = ""
#        flagsum = 0
#        for NAICS_var_2 in range(10):
#            if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index:   
#                if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
#                    count = count + 1
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
#            if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index:  
#                if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
#                    count = count + 1
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
#            if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
#                if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
#                    count = count + 1
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
#
#        if count == 1:
#            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#        if count > 1:
#            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            NAICS_var_2 = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-31"+str(NAICS_var_2) in cbp_erange.index: 
#                    if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#
#                if str(State_var)+"-32"+str(NAICS_var_2) in cbp_erange.index: 
#                    if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#  
#                if str(State_var)+"-33"+str(NAICS_var_2) in cbp_erange.index:  
#                    if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#
#    #NAICS 44-45
#    for NAICS_var in n4list:
#        NAICS_rest_sum = 0
#        count = 0
#        count1_string = ""
#        flagsum = 0
#        for NAICS_var_2 in range(10):
#            if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index:  
#                if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
#                    count = count + 1                    
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
#            if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
#                if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
#                    count = count + 1
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
#        if count == 1:
#            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#        if count > 1:
#            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            NAICS_var_2 = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-44"+str(NAICS_var_2) in cbp_erange.index: 
#                    if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#                if str(State_var)+"-45"+str(NAICS_var_2) in cbp_erange.index:  
#                    if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem   
#
#    #NAICS 48-49
#    for NAICS_var in n5list:
#        NAICS_rest_sum = 0
#        count = 0
#        count1_string = ""
#        flagsum = 0
#        for NAICS_var_2 in range(10):
#            if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
#                if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
#                    count = count + 1                    
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
#            if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
#                if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
#                    count = count + 1
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
#        if count == 1:
#            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#        if count > 1:
#            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            NAICS_var_2 = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-48"+str(NAICS_var_2) in cbp_erange.index:
#                    if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#                if str(State_var)+"-49"+str(NAICS_var_2) in cbp_erange.index: 
#                    if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#    
#    State_var = State_var + 1
#
##Four digit emp
#State_var = 0 
#while State_var < vcount:
#    for i in nlist:
#        for d in range(10):
#            NAICS_var=str(i)+str(d)   
#            NAICS_rest_sum = 0
#            count = 0
#            count1_string = ""
#            flagsum = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
#                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
#                        count = count + 1
#                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
#                    else:
#                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
#            if count == 1:
#                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            if count > 1:
#                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#                NAICS_var_2 = 0
#                for NAICS_var_2 in range(10):
#                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index:
#                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#    State_var = State_var + 1
#
##Five digit emp
#State_var = 0 
#while State_var < vcount:
#    for i in nlist:
#        for d in range(11,100):
#            NAICS_var=str(i)+str(d)
#            NAICS_rest_sum = 0
#            count = 0
#            count1_string = ""
#            flagsum = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
#                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                        count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
#                        count = count + 1
#                        flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
#                    else:
#                        NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
#            if count == 1:
#                cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            if count > 1:
#                NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#                for NAICS_var_2 in range(10):
#                    if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
#                        if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                            cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem 
#    State_var = State_var + 1
#
#
##Six digit emp
#State_var = 0 
#while State_var < vcount:
#    for NAICS_var in naics_list6:   
#        NAICS_rest_sum = 0
#        count = 0
#        count1_string = ""
#        flagsum = 0
#        for NAICS_var_2 in range(10):
#            if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
#                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
#                    count = count + 1
#                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
#                else:
#                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
#        if count == 1:
#            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#        if count > 1:
#            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
#            NAICS_var_2 = 0
#            for NAICS_var_2 in range(10):
#                if str(State_var)+"-"+str(NAICS_var)+str(NAICS_var_2) in cbp_erange.index: 
#                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
#                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
#    State_var = State_var + 1
#
#t2=time.time()
#total_time2=t2-t1
#print(total_time2)    

#Ap variable

#Two digit ap
State_var = 1  
while State_var < vcount:
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
State_var = 0 
while State_var < vcount:
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
State_var = 0 
while State_var < vcount:
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
    State_var = State_var + 1

#Five digit ap
State_var = 0 
while State_var < vcount:
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
    State_var = State_var + 1

#Six digit ap
State_var = 0 
while State_var < vcount:
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
    State_var = State_var + 1
t3=time.time()
total_time3=t3-t1
total_time4=t3-t0
print(total_time3)
print(total_time4)
 #Export filled data
cbp_erange.to_csv(path+'/cbp_erange_cty_1_300.csv')

#Import complete dataset and filter out state and NAICS
#cbp_fill_state = pd.read_csv(path+'/cbp_erange_cty.csv')
##cbp_fill_state['fipstate'] = cbp_fill_state['cty_naics'].apply(lambda x: x.split('-')[0])
#cbp_fill_state['naics'] = cbp_fill_state['cty_naics'].apply(lambda x: x.split('-')[1])
#cbp_fill_state.to_csv(path+'/cbp_fill_state.csv')
