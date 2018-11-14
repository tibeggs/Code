#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import cbp us data
cbp = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/cbp12us.csv')
cbp = cbp[cbp['lfo']=='-'][['naics','empflag','emp','ap','est']]
cbp.info()
cbp.describe()
cbp.head()

#Import employment range data and merge with cbp us data
erange = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/employment_ranges.csv')
erange.head()
cbp_erange = pd.merge(cbp, erange,how='left',on='empflag')
cbp_erange.info()
cbp_erange.head()

#Clean cbp us data and prepare for filling
cbp_erange['naics'] = cbp_erange['naics'].str.replace('/','')
cbp_erange['naics'] = cbp_erange['naics'].str.replace('-','')
cbp_erange.loc[0,'naics'] = 'Total' 
cbp_erange.head()
cbp_erange.set_index('naics',inplace=True)
cbp_erange.head()
print(cbp_erange.loc['Total','emp'])

#Emp variable

#Two digit emp
NAICS_var = 0
NAICS_rest_sum = 0
count = 0
count1_string = ""
while NAICS_var < 100:
    try: 
        if ((cbp_erange.loc[str(NAICS_var),'emp'])==0):
            count1_string = str(NAICS_var)
            count = count + 1
        else:
            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var),'emp']
    except:
        X_test = 0
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc['Total','emp'] - NAICS_rest_sum
    NAICS_var = NAICS_var + 1

#Three digit emp
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
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc['31'+str(NAICS_var_2),'emp'])==0):
               count1_string = '31'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['31'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['31'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['32'+str(NAICS_var_2),'emp'])==0):
               count1_string = '32'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['32'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['32'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['33'+str(NAICS_var_2),'emp'])==0):
               count1_string = '33'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['33'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['33'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc['31'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['31'+str(NAICS_var_2),'emp'] = cbp_erange.loc['31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['32'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['32'+str(NAICS_var_2),'emp'] = cbp_erange.loc['32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['33'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['33'+str(NAICS_var_2),'emp'] = cbp_erange.loc['33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc['44'+str(NAICS_var_2),'emp'])==0):
               count1_string = '44'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['44'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['44'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['45'+str(NAICS_var_2),'emp'])==0):
               count1_string = '45'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['45'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['45'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc['44'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['44'+str(NAICS_var_2),'emp'] = cbp_erange.loc['44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['45'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['45'+str(NAICS_var_2),'emp'] = cbp_erange.loc['45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc['48'+str(NAICS_var_2),'emp'])==0):
               count1_string = '48'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['48'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['48'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['49'+str(NAICS_var_2),'emp'])==0):
               count1_string = '49'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['49'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['49'+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc['48'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['48'+str(NAICS_var_2),'emp'] = cbp_erange.loc['48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['49'+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc['49'+str(NAICS_var_2),'emp'] = cbp_erange.loc['49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1
        
#Four digit emp
NAICS_var = 111
while NAICS_var < 1000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1       

#Five digit emp
NAICS_var = 1111
while NAICS_var < 10000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Six digit emp
NAICS_var = 11111
while NAICS_var < 100000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'emp'] = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'emp'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Ap variable

#Two digit ap
NAICS_var = 0
NAICS_rest_sum = 0
count = 0
count1_string = ""
while NAICS_var < 100:
    try: 
        if ((cbp_erange.loc[str(NAICS_var),'ap'])==0):
            count1_string = str(NAICS_var)
            count = count + 1
        else:
            NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var),'ap']
    except:
        X_test = 0
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc['Total','ap'] - NAICS_rest_sum
    NAICS_var = NAICS_var + 1

#Three digit ap
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
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc['31'+str(NAICS_var_2),'ap'])==0):
               count1_string = '31'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['31'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['31'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['32'+str(NAICS_var_2),'ap'])==0):
               count1_string = '32'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['32'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['32'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['33'+str(NAICS_var_2),'ap'])==0):
               count1_string = '33'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['33'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['33'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc['31'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['31'+str(NAICS_var_2),'ap'] = cbp_erange.loc['31'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['32'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['32'+str(NAICS_var_2),'ap'] = cbp_erange.loc['32'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['33'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['33'+str(NAICS_var_2),'ap'] = cbp_erange.loc['33'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc['44'+str(NAICS_var_2),'ap'])==0):
               count1_string = '44'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['44'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['44'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['45'+str(NAICS_var_2),'ap'])==0):
               count1_string = '45'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['45'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['45'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc['44'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['44'+str(NAICS_var_2),'ap'] = cbp_erange.loc['44'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['45'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['45'+str(NAICS_var_2),'ap'] = cbp_erange.loc['45'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc['48'+str(NAICS_var_2),'ap'])==0):
               count1_string = '48'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['48'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['48'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       try: 
           if ((cbp_erange.loc['49'+str(NAICS_var_2),'ap'])==0):
               count1_string = '49'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc['49'+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc['49'+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc['48'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['48'+str(NAICS_var_2),'ap'] = cbp_erange.loc['48'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((cbp_erange.loc['49'+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc['49'+str(NAICS_var_2),'ap'] = cbp_erange.loc['49'+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
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
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1

#Four digit ap
NAICS_var = 111
while NAICS_var < 1000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1    

#Five digit ap
NAICS_var = 1111
while NAICS_var < 10000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Six digit ap
NAICS_var = 11111
while NAICS_var < 100000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp']
           else:
               NAICS_rest_sum = NAICS_rest_sum + cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        cbp_erange.loc[count1_string,'ap'] = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = cbp_erange.loc[str(NAICS_var),'ap'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'])==0):
                    cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'ap'] = cbp_erange.loc[str(NAICS_var)+str(NAICS_var_2),'emp'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Export filled data
cbp_erange.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/cbp_erange_out.csv')