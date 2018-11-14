#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Import zip code data
zip_code_data = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_breakout_data.csv')
zip_code_data.info()
zip_code_data = zip_code_data[['zip','naics','est','frm','emp','ap','rev']]

#sum all zips by NAICS for each breakout variable
sum_est = zip_code_data.groupby("naics")["est"].sum()
sum_frm = zip_code_data.groupby("naics")["frm"].sum()
sum_emp = zip_code_data.groupby("naics")["emp"].sum()
sum_ap = zip_code_data.groupby("naics")["ap"].sum()
sum_rev = zip_code_data.groupby("naics")["rev"].sum()

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
zip_code_data_merge = zip_code_data
zip_code_data_merge = pd.merge(sum_est,zip_code_data_merge,how='left',on='naics')
zip_code_data_merge = pd.merge(sum_frm,zip_code_data_merge,how='left',on='naics')
zip_code_data_merge = pd.merge(sum_emp,zip_code_data_merge,how='left',on='naics')
zip_code_data_merge = pd.merge(sum_ap,zip_code_data_merge,how='left',on='naics')
zip_code_data_merge = pd.merge(sum_rev,zip_code_data_merge,how='left',on='naics')

#create ratios in dataset
zip_code_data_ratio = zip_code_data_merge
zip_code_data_ratio['est_ratio'] = zip_code_data_ratio['est'] / zip_code_data_ratio['est_sum']
zip_code_data_ratio['frm_ratio'] = zip_code_data_ratio['frm'] / zip_code_data_ratio['frm_sum']
zip_code_data_ratio['emp_ratio'] = zip_code_data_ratio['emp'] / zip_code_data_ratio['emp_sum']
zip_code_data_ratio['ap_ratio'] = zip_code_data_ratio['ap'] / zip_code_data_ratio['ap_sum']
zip_code_data_ratio['rev_ratio'] = zip_code_data_ratio['rev'] / zip_code_data_ratio['rev_sum']

#Drop auxilliary variables from dataset
zip_code_data_ratio = zip_code_data_ratio[['zip','naics','est_ratio','frm_ratio','emp_ratio','ap_ratio','rev_ratio']]

#Export zip code ratio breakout data
zip_code_data_ratio.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_data_ratio.csv')

#Filter out NAICS code to reduce size
zip_code_NAICS_filter = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_data_ratio.csv')
zip_code_NAICS_filter = zip_code_NAICS_filter[['zip','naics','est_ratio','frm_ratio','emp_ratio','ap_ratio','rev_ratio']]
NAICS_Filter = [11,48,325,452,485,1151,2111,2213,3117,3221,32411,32511,32518,42469,42491,45411,48721,48799,48821,48831,48832,54171,211111,211112,237210,238220,238910,311352,311615, \
                311710,321920,325199,325311,325412,325414,332710,333242,333318,334118,334413,334419,334510,334511,334515,335921,336411,336413,336611,336612,339112,339999,423320,423450, \
                423490,423610,423690,423710,423840,423860,423990,424130,424210,424460,424480,424690,424910,425120,441222,441228,441320,445210,445220,445230,445299,446110,451212,453220, \
                453920,481111,481112,481212,481219,483111,483112,483113,483114,483211,483212,484110,484121,484210,484220,484230,485999,487990,488119,488190,488210,488330,488390,488510, \
                488991,488999,492110,493110,493120,493190,512110,519190,522291,523140,523910,523920,523930,531130,531210,532120,532210,532411,541380,541611,541613,541614,541618,541690, \
                541860,541990,561499,561510,561613,561910,561990,562112,611310,611512,611610,621399,621493,621512,621991,624190,711510,712110,712190,713210,713290,713930,722511,811213, \
                811490,812210,812220,813910,'Total']
zip_code_NAICS_filter=zip_code_NAICS_filter[zip_code_NAICS_filter.naics.isin(NAICS_Filter)]
zip_code_NAICS_filter.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_NAICS_filter.csv', index=False)

#Turn dataset long
zip_code_data_ratio_long = zip_code_data = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_NAICS_filter.csv')
zip_code_data_ratio_long['zip_naics'] = zip_code_data_ratio_long['zip'].map(str) + '-' + zip_code_data_ratio_long['naics'].map(str)
zip_code_data_ratio_long = zip_code_data_ratio_long[['zip_naics','est_ratio','frm_ratio','emp_ratio','ap_ratio','rev_ratio']]
zip_code_data_ratio_long.set_index('zip_naics',inplace=True)
zip_code_data_ratio_long = zip_code_data_ratio_long.unstack()
zip_code_data_ratio_long = zip_code_data_ratio_long.to_frame()
zip_code_data_ratio_long = zip_code_data_ratio_long.reset_index()
zip_code_data_ratio_long.columns = ['variable', 'zip_naics','ratio']
zip_code_data_ratio_long['zip_naics_variable'] = zip_code_data_ratio_long['zip_naics'].map(str) + '-' + zip_code_data_ratio_long['variable'].map(str)
zip_code_data_ratio_long = zip_code_data_ratio_long[['zip_naics_variable','ratio']]
zip_code_data_ratio_long.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/zip_code_data_ratio_long.csv')