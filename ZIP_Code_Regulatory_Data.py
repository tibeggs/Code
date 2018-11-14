#Import libraries
import pandas as pd
import numpy as np
import math as ma

#Merge regulatory cost data and geographic data
zip_code_regulatory_costs = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/regulatory_costs.csv')
zip_code_regulatory_costs['lookup'] = zip_code_regulatory_costs['RIN'].map(str) + '-' + zip_code_regulatory_costs['Regulatory_Action_Type'].map(str) + '-' + zip_code_regulatory_costs['Portion'].map(str)
zip_code_regulatory_costs.info()
costs_geo = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/costs_geo.csv')
costs_geo['lookup'] = costs_geo['RIN'].map(str) + '-' + costs_geo['Regulatory_Action_Type'].map(str) + '-' + costs_geo['Portion'].map(str)
costs_geo = costs_geo[['lookup','State','Concept']]
costs_geo.info()
state_regulatory_costs_geo = pd.merge(costs_geo,state_regulatory_costs,how='left',on='lookup')
state_regulatory_costs_geo = state_regulatory_costs_geo[['RIN','Regulatory_Action_Type','Cost Concept','Portion','CFR','NAICS','State','Concept','Cost']]
state_regulatory_costs_geo.info()
state_regulatory_costs_geo.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_costs_geo.csv')

#Create rows for each state
state_regulatory_costs_geo = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_costs_geo.csv')
state_regulatory_costs_geo = state_regulatory_costs_geo[['RIN','Regulatory_Action_Type','Cost Concept','Portion','CFR','NAICS','State','Concept','Cost']]
state_match = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_match.csv')
state_regulatory_costs_geo_match = pd.merge(state_match,state_regulatory_costs_geo,how='left',on='State')
state_regulatory_costs_geo_match=state_regulatory_costs_geo_match.fillna("NA")
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match[state_regulatory_costs_geo_match.RIN != "NA"]
state_regulatory_costs_geo_match['index_string'] = state_regulatory_costs_geo_match['RIN'].map(str)+'@'+state_regulatory_costs_geo_match['Regulatory_Action_Type'].map(str) \
    +'@'+state_regulatory_costs_geo_match['Cost Concept'].map(str)+'@'+state_regulatory_costs_geo_match['Portion'].map(str)+'@'+state_regulatory_costs_geo_match['CFR'].map(str) \
    +'@'+state_regulatory_costs_geo_match['NAICS'].map(str)+'@'+state_regulatory_costs_geo_match['Concept'].map(str)+'@'+state_regulatory_costs_geo_match['Cost'].map(str)
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match.drop(['State','RIN', 'Regulatory_Action_Type','Cost Concept','Portion','CFR','NAICS','Concept','Cost'], axis=1)
state_regulatory_costs_geo_match.set_index('index_string',inplace=True)
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match.unstack()
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match.to_frame()
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match.reset_index()
state_regulatory_costs_geo_match.columns = ['temp', 'index_string','state']
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match.drop(['temp'], axis=1)
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match[state_regulatory_costs_geo_match.state != "NA"]
state_regulatory_costs_geo_match['RIN'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[0])
state_regulatory_costs_geo_match['Regulatory_Action_Type'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[1])
state_regulatory_costs_geo_match['Cost_Concept'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[2])
state_regulatory_costs_geo_match['Portion'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[3])
state_regulatory_costs_geo_match['CFR'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[4])
state_regulatory_costs_geo_match['NAICS'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[5])
state_regulatory_costs_geo_match['Concept'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[6])
state_regulatory_costs_geo_match['Cost'] = state_regulatory_costs_geo_match['index_string'].apply(lambda x: x.split('@')[7])
state_regulatory_costs_geo_match = state_regulatory_costs_geo_match.drop(['index_string'], axis=1)
state_regulatory_costs_geo_match.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_costs_geo_match.csv')

#Create lookup NAICS code to align NAICS between census data and regulatory data
state_regulatory_data_NAICS_lookup = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_costs_geo_match.csv')
state_regulatory_data_NAICS_lookup = state_regulatory_data_NAICS_lookup[['state','RIN','Regulatory_Action_Type','Cost_Concept','Portion','CFR','NAICS','Concept','Cost']]
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS'].astype('int64')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].astype(str)
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('111998','11')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('112340','11')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('325181','32518')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('325188','32518')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('441229','441228')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('452319','452')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('454110','45411')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('482111','48')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('482112','48')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('541714','54171')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('541715','54171')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('926120','Total')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('999998','Total')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].str.replace('999999','Total')
state_regulatory_data_NAICS_lookup['NAICS_lookup'] = state_regulatory_data_NAICS_lookup['NAICS_lookup'].replace(['92'], 'Total')
state_regulatory_data_NAICS_lookup.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_data_NAICS_lookup.csv')

#Get variable ratios for regulatory data
state_regulatory_data = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_data_NAICS_lookup.csv')
state_regulatory_data = state_regulatory_data[['state','RIN','Regulatory_Action_Type','Cost_Concept','Portion','CFR','NAICS','NAICS_lookup','Concept','Cost']]
state_regulatory_data['Concept'] = state_regulatory_data['Concept'].str.replace('Establishments','est_ratio')
state_regulatory_data['Concept'] = state_regulatory_data['Concept'].str.replace('Revenue','rev_ratio')
state_regulatory_data['Concept'] = state_regulatory_data['Concept'].str.replace('Firms','frm_ratio')
state_regulatory_data['Concept'] = state_regulatory_data['Concept'].str.replace('Payroll','ap_ratio')
state_regulatory_data['Concept'] = state_regulatory_data['Concept'].str.replace('Employment','emp_ratio')
state_regulatory_data['state'] = state_regulatory_data['state'].astype('int64')
state_regulatory_data['state_naics_variable'] = state_regulatory_data['state'].map(str)+'-'+state_regulatory_data['NAICS_lookup'].map(str)+'-'+state_regulatory_data['Concept'].map(str)
state_data_ratio_long = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_data_ratio_long.csv')
state_regulatory_data = pd.merge(state_data_ratio_long,state_regulatory_data,how='left',on='state_naics_variable')
state_regulatory_data=state_regulatory_data.fillna("NA")
state_regulatory_data = state_regulatory_data[state_regulatory_data.state != "NA"]
state_regulatory_data.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_data.csv')

#Include summed variables
state_regulatory_data = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_regulatory_data.csv')
state_regulatory_data = state_regulatory_data[['RIN','Regulatory_Action_Type','Cost_Concept','Portion','CFR','NAICS','state','Cost','ratio']]
state_regulatory_data['index_string'] = state_regulatory_data['RIN'].map(str)+'@'+state_regulatory_data['Regulatory_Action_Type'].map(str) \
    +'@'+state_regulatory_data['Cost_Concept'].map(str)+'@'+state_regulatory_data['Portion'].map(str)+'@'+state_regulatory_data['CFR'].map(str)+'@'+state_regulatory_data['NAICS'].map(str)
sum_var = state_regulatory_data.groupby("index_string")["ratio"].sum()
sum_var = sum_var.to_frame()
sum_var['ratio_sum'] = sum_var['ratio']
sum_var = sum_var.drop(['ratio'], axis=1)
state_reg_data_sum = pd.merge(sum_var,state_regulatory_data,how='left',on='index_string')
state_reg_data_sum.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_reg_data_sum.csv')

#Calculate shared out regulatory costs
state_reg_data_sum = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_reg_data_sum.csv')
state_reg_data_sum = state_reg_data_sum[['RIN','Regulatory_Action_Type','Cost_Concept','state','CFR','NAICS','Cost','ratio','ratio_sum']]
state_reg_data_sum['state_reg_cost'] = state_reg_data_sum['ratio'] / state_reg_data_sum['ratio_sum'] * state_reg_data_sum['Cost']
state_reg_data = state_reg_data_sum.drop(['ratio','ratio_sum','Cost'], axis=1)
state_reg_data.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_reg_data.csv')

#Match state codes to state
state_reg_data_final = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_reg_data.csv')
state_fips = pd.read_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_fips.csv')
state_reg_data_final = pd.merge(state_fips,state_reg_data_final,how='left',on='state')
state_reg_data_final = state_reg_data_final[['RIN','Regulatory_Action_Type','Cost_Concept','State_Name','CFR','NAICS','state_reg_cost']]
state_reg_data_final['NAICS'] = state_reg_data_final['NAICS'].astype('int64')
state_reg_data_final['NAICS'] = 'NAICS ' + state_reg_data_final['NAICS'].astype(str)
state_reg_data_final.to_csv('C:/Users/jdavis/OneDrive - ECONOMETRICA INC/Projects/TSA/Regulatory Database - Phase II/Python/Geo_Datasets/state_reg_data_final.csv', index=False)



