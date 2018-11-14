#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import susb us data
susb = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb12us.csv')
susb = susb[['NAICS','FIRM','ESTB','EMPL_N','PAYR_N','RCPT_N','EMPLFL_R']]
susb = susb.rename(index=str, columns={"EMPLFL_R": "empflag"})
susb.info()
susb.describe()
susb.head()

#Import employment range data and merge with cbp us data
erange = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/employment_ranges.csv')
erange.head()
susb_erange = pd.merge(susb, erange,how='left',on='empflag')
susb_erange = susb_erange[['NAICS','FIRM','ESTB','EMPL_N','PAYR_N','RCPT_N','e_range']]
susb_erange.info()
susb_erange.head()

#Clean susb us data and prepare for filling
susb_erange['NAICS'] = susb_erange['NAICS'].str.replace('/','')
susb_erange['NAICS'] = susb_erange['NAICS'].str.replace('-','')
susb_erange.loc[0,'NAICS'] = 'Total' 
susb_erange['NAICS'] = susb_erange['NAICS'].str.replace('31-33','31')
susb_erange['NAICS'] = susb_erange['NAICS'].str.replace('44-45','44')
susb_erange['NAICS'] = susb_erange['NAICS'].str.replace('48-49','48')
susb_erange.head()
susb_erange.set_index('NAICS',inplace=True)
susb_erange.head()

#EMPL_N variable

#Two digit EMPL_N
NAICS_var = 0
NAICS_rest_sum = 0
count = 0
count1_string = ""
while NAICS_var < 100:
    try: 
        if ((susb_erange.loc[str(NAICS_var),'EMPL_N'])==0):
            count1_string = str(NAICS_var)
            count = count + 1
        else:
            NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var),'EMPL_N']
    except:
        X_test = 0
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc['Total','EMPL_N'] - NAICS_rest_sum
    NAICS_var = NAICS_var + 1

#Three digit EMPL_N
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '31'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['31'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '32'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['32'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '33'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['33'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['31'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['32'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['33'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '44'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['44'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '45'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['45'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['44'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['45'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '48'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['48'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = '49'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['49'+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['48'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc['49'+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1
        
#Four digit EMPL_N
NAICS_var = 111
while NAICS_var < 1000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1       

#Five digit EMPL_N
NAICS_var = 1111
while NAICS_var < 10000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Six digit EMPL_N
NAICS_var = 11111
while NAICS_var < 100000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'EMPL_N'] = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'EMPL_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'e_range'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#PAYR_N variable

#Two digit PAYR_N
NAICS_var = 0
NAICS_rest_sum = 0
count = 0
count1_string = ""
while NAICS_var < 100:
    try: 
        if ((susb_erange.loc[str(NAICS_var),'PAYR_N'])==0):
            count1_string = str(NAICS_var)
            count = count + 1
        else:
            NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var),'PAYR_N']
    except:
        X_test = 0
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc['Total','PAYR_N'] - NAICS_rest_sum
    NAICS_var = NAICS_var + 1

#Three digit PAYR_N
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['31'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '31'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['31'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['32'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '32'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['32'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['33'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '33'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['33'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['31'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['31'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['32'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['32'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['33'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['33'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['44'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '44'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['44'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['45'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '45'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['45'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['44'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['44'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['45'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['45'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['48'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '48'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['48'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['49'+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = '49'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['49'+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['48'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['48'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['49'+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc['49'+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1
        
#Four digit PAYR_N
NAICS_var = 111
while NAICS_var < 1000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1       

#Five digit PAYR_N
NAICS_var = 1111
while NAICS_var < 10000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Six digit PAYR_N
NAICS_var = 11111
while NAICS_var < 100000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'PAYR_N'] = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'PAYR_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'PAYR_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#RCPT_N variable

#Two digit RCPT_N
NAICS_var = 0
NAICS_rest_sum = 0
count = 0
count1_string = ""
while NAICS_var < 100:
    try: 
        if ((susb_erange.loc[str(NAICS_var),'RCPT_N'])==0):
            count1_string = str(NAICS_var)
            count = count + 1
        else:
            NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var),'RCPT_N']
    except:
        X_test = 0
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc['Total','RCPT_N'] - NAICS_rest_sum
    NAICS_var = NAICS_var + 1

#Three digit RCPT_N
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['31'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '31'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['31'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['32'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '32'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['32'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['33'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '33'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['33'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['31'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['31'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['31'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['32'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['32'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['32'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['33'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['33'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['33'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['44'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '44'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['44'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['45'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '45'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['45'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['44'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['44'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['44'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['45'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['45'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['45'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc['48'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '48'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['48'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       try: 
           if ((susb_erange.loc['49'+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = '49'+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc['49'+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc['48'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['48'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['48'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            try: 
                if ((susb_erange.loc['49'+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc['49'+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc['49'+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
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
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1
        
#Four digit RCPT_N
NAICS_var = 111
while NAICS_var < 1000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1       

#Five digit RCPT_N
NAICS_var = 1111
while NAICS_var < 10000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Six digit RCPT_N
NAICS_var = 11111
while NAICS_var < 100000:
    NAICS_var_2 = 0
    NAICS_rest_sum = 0
    count = 0
    count1_string = ""
    flagsum = 0
    while NAICS_var_2 < 10:
       try: 
           if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
               count1_string = str(NAICS_var)+str(NAICS_var_2)
               count = count + 1
               flagsum = flagsum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N']
           else:
               NAICS_rest_sum = NAICS_rest_sum + susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N']
       except:
           X_test = 0
       NAICS_var_2 = NAICS_var_2 + 1
    if count == 1:
        susb_erange.loc[count1_string,'RCPT_N'] = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
    if count > 1:
        NAICS_rem = susb_erange.loc[str(NAICS_var),'RCPT_N'] - NAICS_rest_sum
        NAICS_var_2 = 1
        while NAICS_var_2 < 10:
            try: 
                if ((susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'])==0):
                    susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'RCPT_N'] = susb_erange.loc[str(NAICS_var)+str(NAICS_var_2),'EMPL_N'] / flagsum * NAICS_rem
            except:
                X_test = 0    
            NAICS_var_2 = NAICS_var_2 + 1
    NAICS_var = NAICS_var + 1   

#Export filled data
susb_erange.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb_erange_out.csv')