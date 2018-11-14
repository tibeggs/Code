#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import cbp state data
path = "M:\\TSA\\c.tasks\\Task 17 UpdatingRegDatabasePhase2\\Python\\Geo_Datasets"
cbp = pd.read_csv(path +'/cbp12st_compact.csv')
cbp = cbp[['fipstate','naics','empflag','emp','ap','est']]
cbp.info()
cbp.describe()
cbp.head()

#Import employment range data and merge with cbp state data
erange = pd.read_csv(path+ '/employment_ranges.csv')
erange.head()
cbp_erange = pd.merge(cbp, erange,how='left',on='empflag')
cbp_erange.info()
cbp_erange.head()

#Clean cbp state data and prepare for filling
cbp_erange['naics'] = cbp_erange['naics'].str.replace('------','Total')
cbp_erange['naics'] = cbp_erange['naics'].str.replace('/','')
cbp_erange['naics'] = cbp_erange['naics'].str.replace('-','')
cbp_erange['state_naics'] = cbp_erange['fipstate'].map(str) + '-' + cbp_erange['naics'].map(str)
cbp_erange.head()
cbp_erange = cbp_erange[['e_range','emp','ap','est','state_naics']]
cbp_erange.set_index('state_naics',inplace=True)
cbp_erange.head()

list(cbp)
cbp.head()

#Emp variable

#Two digit emp
State_var = 1  
while State_var < 60:
    NAICS_var = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0    
    while NAICS_var < 100:
        try: 
            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
                count1_string = str(State_var)+'-'+str(NAICS_var)
                count = count + 1
                flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']
            else:
                NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
        except:
            X_test = 0
        NAICS_var = NAICS_var + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_var = 0
        NAICS_rem = cbp_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
        while NAICS_var < 100:           
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0
            NAICS_var = NAICS_var + 1
    State_var = State_var + 1

#Three digit emp
State_var = 0 
while State_var < 60:
    #NAICS 11-23
    NAICS_var = 11
    while NAICS_var < 24:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    #NAICS 31-33
    NAICS_var = 31
    while NAICS_var == 31:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                    count = count + 1
                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1         
    #NAICS 42
    NAICS_var = 42
    while NAICS_var == 42:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1  
    #NAICS 44-45
    NAICS_var = 44
    while NAICS_var == 44:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    #NAICS 48-49
    NAICS_var = 48
    while NAICS_var == 48:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    #NAICS 51+
    NAICS_var = 50
    while NAICS_var < 100:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1       
    State_var = State_var + 1

#Four digit emp
State_var = 0 
while State_var < 60:
    NAICS_var = 111
    while NAICS_var < 1000:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Five digit emp
State_var = 0 
while State_var < 60:
    NAICS_var = 1111
    while NAICS_var < 10000:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Six digit emp
State_var = 0 
while State_var < 60:
    NAICS_var = 11111
    while NAICS_var < 100000:   
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Ap variable

#Two digit ap
State_var = 1  
while State_var < 60:
    NAICS_var = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0    
    while NAICS_var < 100:
        try: 
            if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'])==0):
                count1_string = str(State_var)+'-'+str(NAICS_var)
                count = count + 1
                flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
            else:
                NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap']
        except:
            X_test = 0
        NAICS_var = NAICS_var + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-Total','ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_var = 0
        NAICS_rem = cbp_erange.loc[str(State_var)+'-Total','ap'] - NAICS_rest_sum
        while NAICS_var < 100:           
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'])==0):
                    cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0
            NAICS_var = NAICS_var + 1
    State_var = State_var + 1

#Three digit ap
State_var = 0 
while State_var < 60:
    #NAICS 11-23
    NAICS_var = 11
    while NAICS_var < 24:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    #NAICS 31-33
    NAICS_var = 31
    while NAICS_var == 31:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                    count = count + 1
                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1         
    #NAICS 42
    NAICS_var = 42
    while NAICS_var == 42:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1  
    #NAICS 44-45
    NAICS_var = 44
    while NAICS_var == 44:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    #NAICS 48-49
    NAICS_var = 48
    while NAICS_var == 48:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    #NAICS 51+
    NAICS_var = 50
    while NAICS_var < 100:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1       
    State_var = State_var + 1

#Four digit ap
State_var = 0 
while State_var < 60:
    NAICS_var = 111
    while NAICS_var < 1000:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Five digit ap
State_var = 0 
while State_var < 60:
    NAICS_var = 1111
    while NAICS_var < 10000:
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Six digit ap
State_var = 0 
while State_var < 60:
    NAICS_var = 11111
    while NAICS_var < 100000:   
        NAICS_var_2 = 0
        NAICS_rest_sum = 0
        count = 0
        count1_string = ""
        flagsum = 0
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

 #Export filled data
cbp_erange.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/cbp_erange_state.csv')

#Import complete dataset and filter out state and NAICS
cbp_fill_state = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/cbp_erange_state.csv')
cbp_fill_state['fipstate'] = cbp_fill_state['state_naics'].apply(lambda x: x.split('-')[0])
cbp_fill_state['naics'] = cbp_fill_state['state_naics'].apply(lambda x: x.split('-')[1])
cbp_fill_state.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/cbp_fill_state.csv')
