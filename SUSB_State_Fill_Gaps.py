#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import susb state data
susb = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/subs12st_compact.csv')
susb = susb[['NAICS','FIRM','ESTB','EMPL_N','PAYR_N','RCPT_N','EMPLFL_R','STATE']]
susb = susb.rename(index=str, columns={"EMPLFL_R": "empflag", "STATE": "fipstate", "NAICS": "naics", "FIRM": "frm", "ESTB": "est"})
susb = susb.rename(index=str, columns={"EMPL_N": "emp", "PAYR_N": "ap", "RCPT_N": "rev"})
susb.info()
susb.describe()
susb.head()

#Import employment range data and merge with susb state data
erange = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/employment_ranges.csv')
erange.head()
susb_erange = pd.merge(susb, erange,how='left',on='empflag')
susb_erange.info()
susb_erange.head()

#Clean cbp state data and prepare for filling
susb_erange['naics'] = susb_erange['naics'].str.replace('31-33','31')
susb_erange['naics'] = susb_erange['naics'].str.replace('44-45','44')
susb_erange['naics'] = susb_erange['naics'].str.replace('48-49','48')
susb_erange['naics'] = susb_erange['naics'].str.replace('--','Total')
susb_erange['naics'] = susb_erange['naics'].str.replace('/','')
susb_erange['naics'] = susb_erange['naics'].str.replace('-','')
susb_erange['state_naics'] = susb_erange['fipstate'].map(str) + '-' + susb_erange['naics'].map(str)
susb_erange.head()
susb_erange = susb_erange[['e_range','emp','ap','est','frm','rev','state_naics']]
susb_erange.set_index('state_naics',inplace=True)
susb_erange.head()

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
            if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
                count1_string = str(State_var)+'-'+str(NAICS_var)
                count = count + 1
                flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range']
            else:
                NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
        except:
            X_test = 0
        NAICS_var = NAICS_var + 1
    if count == 1:
        susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_var = 0
        NAICS_rem = susb_erange.loc[str(State_var)+'-Total','emp'] - NAICS_rest_sum
        while NAICS_var < 100:           
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'])==0):
                    susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                    count = count + 1
                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#ap variable

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
            if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'])==0):
                count1_string = str(State_var)+'-'+str(NAICS_var)
                count = count + 1
                flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
            else:
                NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap']
        except:
            X_test = 0
        NAICS_var = NAICS_var + 1
    if count == 1:
        susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-Total','ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_var = 0
        NAICS_rem = susb_erange.loc[str(State_var)+'-Total','ap'] - NAICS_rest_sum
        while NAICS_var < 100:           
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'])==0):
                    susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                    count = count + 1
                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'ap'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'ap'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#rev variable

#Two digit rev
State_var = 1  
while State_var < 60:
    NAICS_var = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0    
    while NAICS_var < 100:
        try: 
            if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'])==0):
                count1_string = str(State_var)+'-'+str(NAICS_var)
                count = count + 1
                flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp']
            else:
                NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev']
        except:
            X_test = 0
        NAICS_var = NAICS_var + 1
    if count == 1:
        susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-Total','rev'] - NAICS_rest_sum
    if count > 1:
        NAICS_var = 0
        NAICS_rem = susb_erange.loc[str(State_var)+'-Total','rev'] - NAICS_rest_sum
        while NAICS_var < 100:           
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'])==0):
                    susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0
            NAICS_var = NAICS_var + 1
    State_var = State_var + 1

#Three digit rev
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'31'+str(NAICS_var_2)
                    count = count + 1
                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'32'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'33'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'31'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'32'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'33'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'44'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'45'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'44'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'45'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'48'+str(NAICS_var_2)
                    count = count + 1                    
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            try: 
                if ((susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+'49'+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'48'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+'49'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1       
    State_var = State_var + 1

#Four digit rev
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1
    
#Five digit rev
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Six digit rev
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
                if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                    count1_string = str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2)
                    count = count + 1
                    flagsum = flagsum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp']
                else:
                    NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev']
            except:
                X_test = 0
            NAICS_var_2 = NAICS_var_2 + 1
        if count == 1:
            susb_erange.loc[count1_string,'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
        if count > 1:
            NAICS_rem = susb_erange.loc[str(State_var)+'-'+str(NAICS_var),'rev'] - NAICS_rest_sum
            NAICS_var_2 = 0
            while NAICS_var_2 < 10:
                try: 
                    if ((susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'])==0):
                        susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'rev'] = susb_erange.loc[str(State_var)+'-'+str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
                except:
                    X_test = 0    
                NAICS_var_2 = NAICS_var_2 + 1
        NAICS_var = NAICS_var + 1   
    State_var = State_var + 1

#Export filled data
susb_erange.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb_erange_state.csv')

#Import complete dataset and filter out state and NAICS
susb_fill_state = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb_erange_state.csv')
susb_fill_state['fipstate'] = susb_fill_state['state_naics'].apply(lambda x: x.split('-')[0])
susb_fill_state['naics'] = susb_fill_state['state_naics'].apply(lambda x: x.split('-')[1])
susb_fill_state.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb_fill_state.csv')
