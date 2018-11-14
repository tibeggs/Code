#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import cbp zip code data and clean
cbp_zip_data = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/cbp_zipcode.csv')
cbp_zip_data['naics'] = cbp_zip_data['naics'].str.replace('------','Total')
cbp_zip_data['naics'] = cbp_zip_data['naics'].str.replace('/','')
cbp_zip_data['naics'] = cbp_zip_data['naics'].str.replace('-','')
cbp_zip_data.info()
cbp_zip_data.describe()
cbp_zip_data.head()

#Check which zip codes are included
zip_group = cbp_zip_data.groupby(['zip']).count()
zip_group.head()
zip_group.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_group.csv')

#Import state zip code correspondance sheet
state_zip_code = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_zip_code.csv')
state_zip_code = state_zip_code[['fipstate','zip']]
state_zip_code.head()

#Assign states to each zip code in cbp zip code data 
cbp_zs = pd.merge(cbp_zip_data, state_zip_code,how='left',on='zip')
cbp_zs['state_naics'] = cbp_zs['fipstate'].map(str) + '-' + cbp_zs['naics'].map(str)
cbp_zs = cbp_zs[['zip','state_naics','est']]
cbp_zs.head()

#Import susb state data and create ratios
susb_state = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb_state_data_finished.csv')
susb_state['eratio'] = susb_state['emp'] /  susb_state['est']
susb_state['aratio'] = susb_state['ap'] /  susb_state['est']
susb_state['rratio'] = susb_state['rev'] /  susb_state['est']
susb_state['fratio'] = susb_state['frm'] /  susb_state['est']
susb_state['state_naics'] = susb_state['fipstate'].map(str) + '-' + susb_state['naics'].map(str)
susb_state = susb_state[['state_naics','eratio','aratio','rratio','fratio']]
susb_state.head()

#Assign ratios the susb zip code data and use to estimate employment and payroll
zip_data = pd.merge(cbp_zs, susb_state,how='left',on='state_naics')
zip_data['emp'] = zip_data['eratio'] * zip_data['est']
zip_data['ap'] = zip_data['aratio'] * zip_data['est']
zip_data['rev'] = zip_data['rratio'] * zip_data['est']
zip_data['frm'] = zip_data['fratio'] * zip_data['est']
zip_data['fipstate'] = zip_data['state_naics'].apply(lambda x: x.split('-')[0])
zip_data['naics'] = zip_data['state_naics'].apply(lambda x: x.split('-')[1])
zip_data = zip_data[['zip','fipstate','naics','est','frm','emp','ap','rev']]
zip_data.info()
zip_data.describe()
zip_data.head()

#Export zip code cost concept data
zip_data.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_breakout_data.csv')

#Analyze by state
zip_data_all = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_breakout_data.csv')
zip_data_all.head()
zip_data_23 = zip_data_all[zip_data_all['fipstate']==23]
zip_data_23.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_breakout_data_23.csv')
