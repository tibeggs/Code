#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import state data
state_data = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/susb_fill_state.csv')
state_data.info()
state_data = state_data[['fipstate','naics','est','frm','emp','ap','rev']]

#sum all states by NAICS for each breakout variable
sum_est = state_data.groupby("naics")["est"].sum()
sum_frm = state_data.groupby("naics")["frm"].sum()
sum_emp = state_data.groupby("naics")["emp"].sum()
sum_ap = state_data.groupby("naics")["ap"].sum()
sum_rev = state_data.groupby("naics")["rev"].sum()

#Transforms sum datasets from series to frames
sum_est = sum_est.to_frame()
sum_frm = sum_frm.to_frame()
sum_emp = sum_emp.to_frame()
sum_ap = sum_ap.to_frame()
sum_rev = sum_rev.to_frame()

#rename variable names
sum_est['est_sum'] = sum_est['est']
sum_frm['frm_sum'] = sum_frm['frm']
sum_emp['emp_sum'] = sum_emp['emp']
sum_ap['ap_sum'] = sum_ap['ap']
sum_rev['rev_sum'] = sum_rev['rev']

#drop original variable names
sum_est = sum_est[['est_sum']]
sum_frm = sum_frm[['frm_sum']]
sum_emp = sum_emp[['emp_sum']]
sum_ap = sum_ap[['ap_sum']]
sum_rev = sum_rev[['rev_sum']]

#merge summed variables into main dataset
state_data_merge = state_data
state_data_merge = pd.merge(sum_est,state_data_merge,how='left',on='naics')
state_data_merge = pd.merge(sum_frm,state_data_merge,how='left',on='naics')
state_data_merge = pd.merge(sum_emp,state_data_merge,how='left',on='naics')
state_data_merge = pd.merge(sum_ap,state_data_merge,how='left',on='naics')
state_data_merge = pd.merge(sum_rev,state_data_merge,how='left',on='naics')

#create ratios in dataset
state_data_ratio = state_data_merge
state_data_ratio['est_ratio'] = state_data_ratio['est'] / state_data_ratio['est_sum']
state_data_ratio['frm_ratio'] = state_data_ratio['frm'] / state_data_ratio['frm_sum']
state_data_ratio['emp_ratio'] = state_data_ratio['emp'] / state_data_ratio['emp_sum']
state_data_ratio['ap_ratio'] = state_data_ratio['ap'] / state_data_ratio['ap_sum']
state_data_ratio['rev_ratio'] = state_data_ratio['rev'] / state_data_ratio['rev_sum']
state_data_ratio.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_data_ratio.csv')

#Turn dataset long
state_data_ratio_long = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_data_ratio.csv')
state_data_ratio_long = state_data_ratio_long[['fipstate','naics','est_ratio','frm_ratio','emp_ratio','ap_ratio','rev_ratio']]
state_data_ratio_long['state_naics'] = state_data_ratio_long['fipstate'].map(str) + '-' + state_data_ratio_long['naics'].map(str)
state_data_ratio_long = state_data_ratio_long[['state_naics','est_ratio','frm_ratio','emp_ratio','ap_ratio','rev_ratio']]
state_data_ratio_long.set_index('state_naics',inplace=True)
state_data_ratio_long = state_data_ratio_long.unstack()
state_data_ratio_long = state_data_ratio_long.to_frame()
state_data_ratio_long = state_data_ratio_long.reset_index()
state_data_ratio_long.columns = ['variable', 'state_naics','ratio']
state_data_ratio_long['state_naics_variable'] = state_data_ratio_long['state_naics'].map(str) + '-' + state_data_ratio_long['variable'].map(str)
state_data_ratio_long = state_data_ratio_long[['state_naics_variable','ratio']]

#Export state ratio breakout data
state_data_ratio_long.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_data_ratio_long.csv')