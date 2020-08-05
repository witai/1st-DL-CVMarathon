#!/usr/bin/env python
# coding: utf-8

# * The cell below is to import the required packages for running the program.

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
import math


# * The cell below is for the users to setting up the paths and file to be stored.
#     * path = the current working path or the path of the working folder. 
#     * folder name = the folder name where the Jupyter notebook and the bank statement raw data are saved.
#     * bs_tran_name = the downloaded csv storing daily transactions from the bank statement.
#     * bs_daily_bal_name = the downloaded csv storing day-end balance amount

# In[59]:


#Setup the Paths/File Names
path = '/Users/wilsontai/Serai_Bank_Statement_Application/'
folder_name = 'ASTRUM_20191207'
bs_tran_name = 'ASTRUM_RAW_DAILY_BS_TRAN_CA.csv'
bs_daily_bal_name = 'ASTRUM_RAW_DAILY_BS_ACCT_BAL.csv'


# * The cell below is for setting up/defining the time window for every 30 days in the most recent 6 months. The reason being is that the bank statement scorecard is based on the cashflow behaviors across the most recent 6 months (e.g. total day-end balance amount in the last 6 months means the number sums up the day-end balance amount for the most recent 6 months, as a result, "recent 6 months" needs to be well-defined by a start date and a end date)
#     * In current model setting, we define:
#         * M1 as the calendar month 1 month before the current calendar month
#         * M2 as the calendar month 2 months before current calendar month
#         * ...and so on.

# In[9]:


#Create timestamps for M1-M6
#Def M1 as the calendar month 1 month before the current calendar month
#    M2 as the calendar month 2 months before current calendar month
M1_start_dt = '09/27/2019'
M1_end_dt = '10/26/2019'
M2_start_dt = '08/28/2019'
M2_end_dt = '09/26/2019'
M3_start_dt = '07/29/2019'
M3_end_dt = '08/27/2019'
M4_start_dt = '06/29/2019'
M4_end_dt = '07/28/2019'
M5_start_dt = '05/30/2019'
M5_end_dt = '06/28/2019'
M6_start_dt = '04/30/2019' 
M6_end_dt = '05/29/2019'


# In[4]:


#Import raw bank statement transaction data
df_DAILY_BS_TRAN_CA = pd.read_csv(path+folder_name+'/'+bs_tran_name,sep = ',',header = 0)


# In[6]:


#Import raw account level data and keep the unique keys only
df_DAILY_BS_ACCT = pd.read_csv(path+folder_name+'/'+bs_daily_bal_name,sep = ',',header = 0)


# In[7]:


df_DAILY_BS_TRAN_CA.head()


# In[10]:


#Creating DAY-END BALANCE related variable
#Convert the string datetime to Pandas Datetime format for further calculation
tran_date_rng = pd.to_datetime(df_DAILY_BS_TRAN_CA['TRAN_DT'], format = '%d/%m/%Y')
df_DAILY_BS_TRAN_CA['TRAN_DT'] = tran_date_rng
df_DAILY_BS_TRAN_CA['TRAN_DT'].dtype


# In[11]:


#Creating New Time Stamp Columns for Time-Series Based Calculations
time_stamp_str = ['M1_START_DT','M1_END_DT','M2_START_DT','M2_END_DT','M3_START_DT','M3_END_DT','M4_START_DT','M4_END_DT',                  'M5_START_DT','M5_END_DT','M6_START_DT','M6_END_DT']
time_stamp_val = [M1_start_dt,M1_end_dt,M2_start_dt,M2_end_dt,M3_start_dt,M3_end_dt,                  M4_start_dt,M4_end_dt,M5_start_dt,M5_end_dt,M6_start_dt,M6_end_dt]


# In[12]:


df_DAILY_BS_TRAN_CA = df_DAILY_BS_TRAN_CA.reindex(columns=df_DAILY_BS_TRAN_CA.columns.tolist() + time_stamp_str)   # add empty cols
df_DAILY_BS_TRAN_CA[time_stamp_str] = time_stamp_val


# In[13]:


df_DAILY_BS_TRAN_CA.head()


# In[14]:


df_DAILY_BS_TRAN_CA.shape


# In[15]:


#Convert the other string datetime to Pandas Datetime format for further calculation
df_DAILY_BS_TRAN_CA[time_stamp_str] = df_DAILY_BS_TRAN_CA[time_stamp_str].apply(pd.to_datetime, errors='coerce')


# In[16]:


#Convert the numeric fields to float in data frame
#Define the numeric field names
num_attr_str = ['INFLOW_TRAN_AMT_HKD','OUTFLOW_TRAN_AMT_HKD','CAL_BAL_AMT_HKD']
df_DAILY_BS_TRAN_CA[num_attr_str] = df_DAILY_BS_TRAN_CA[num_attr_str].apply(pd.to_numeric, downcast='float')


# In[17]:


#Remove manually excluded transactions
df_DAILY_BS_TRAN_CA = df_DAILY_BS_TRAN_CA[df_DAILY_BS_TRAN_CA['MANUAL_EXCLUSION'] == 0]


# In[18]:


#Creating a Master Account Table
df_ACCT_MAST = df_DAILY_BS_TRAN_CA[['CUST_ID','CUST_NAME','ACCT_ID','ACCT_TYP']].drop_duplicates().sort_values(['CUST_ID','CUST_NAME','ACCT_ID','ACCT_TYP'])
df_ACCT_MAST_STG1 = df_DAILY_BS_TRAN_CA[['CUST_ID','CUST_NAME','ACCT_ID','ACCT_TYP']].drop_duplicates().sort_values(['CUST_ID','CUST_NAME','ACCT_ID','ACCT_TYP'])
df_ACCT_MAST.head()


# In[19]:


#Creating Standard Deviation of INFLOW_TRAN_AMT_HKD & OUTFLOW_TRAN_AMT_HKD
STD_INFLOW_TRAN_AMT_HKD = df_DAILY_BS_TRAN_CA['INFLOW_TRAN_AMT_HKD'].std()
STD_OUTFLOW_TRAN_AMT_HKD = df_DAILY_BS_TRAN_CA['OUTFLOW_TRAN_AMT_HKD'].std()
MEAN_INFLOW_TRAN_AMT_HKD = df_DAILY_BS_TRAN_CA['INFLOW_TRAN_AMT_HKD'].mean()
MEAN_OUTFLOW_TRAN_AMT_HKD = df_DAILY_BS_TRAN_CA['OUTFLOW_TRAN_AMT_HKD'].mean()


# In[20]:


#Creating TRANSACTION Related Variable
#Def Condition Functions
#Function Name: MONTHLY_TRAN_SMRY
#Function Description: This function sets up the conditions for aggregating OUTFLOW & outflow attributes for last 6 months
def MONTHLY_TRAN_SMRY(x):
   names = {
       'TTL_REV_AMT_M1': x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['REVENUE_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_REV_AMT_M2': x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['REVENUE_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_REV_AMT_M3': x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['REVENUE_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_REV_AMT_M4': x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['REVENUE_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_REV_AMT_M5': x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['REVENUE_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_REV_AMT_M6': x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['REVENUE_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_INFLOW_AMT_M1': x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT'])]['INFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_INFLOW_CNT_M1': x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['INFLOW_TRAN_AMT_HKD'].count(),
       'TTL_INFLOW_AMT_M2': x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT'])]['INFLOW_TRAN_AMT_HKD'].sum(),  
       'TTL_INFLOW_CNT_M2': x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['INFLOW_TRAN_AMT_HKD'].count(),
       'TTL_INFLOW_AMT_M3': x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT'])]['INFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_INFLOW_CNT_M3': x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['INFLOW_TRAN_AMT_HKD'].count(),
       'TTL_INFLOW_AMT_M4': x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT'])]['INFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_INFLOW_CNT_M4': x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['INFLOW_TRAN_AMT_HKD'].count(),
       'TTL_INFLOW_AMT_M5': x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT'])]['INFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_INFLOW_CNT_M5': x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['INFLOW_TRAN_AMT_HKD'].count(),
       'TTL_INFLOW_AMT_M6': x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT'])]['INFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_INFLOW_CNT_M6': x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['INFLOW_TRAN_AMT_HKD'].count(),
       'TTL_OUTFLOW_AMT_M1': x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_OUTFLOW_CNT_M1': x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['OUTFLOW_TRAN_AMT_HKD'].count(),
       'TTL_OUTFLOW_AMT_M2': x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_OUTFLOW_CNT_M2': x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['OUTFLOW_TRAN_AMT_HKD'].count(),
       'TTL_OUTFLOW_AMT_M3': x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'TTL_OUTFLOW_CNT_M3': x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['OUTFLOW_TRAN_AMT_HKD'].count(),
       'TTL_OUTFLOW_AMT_M4': x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_OUTFLOW_CNT_M4': x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['OUTFLOW_TRAN_AMT_HKD'].count(),
       'TTL_OUTFLOW_AMT_M5': x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_OUTFLOW_CNT_M5': x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['OUTFLOW_TRAN_AMT_HKD'].count(),
       'TTL_OUTFLOW_AMT_M6': x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].sum(),   
       'TTL_OUTFLOW_CNT_M6': x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['OUTFLOW_TRAN_AMT_HKD'].count(),
       'MAX_INFLOW_TRAN_AMT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT'])]['INFLOW_TRAN_AMT_HKD'].max(),
       'MAX_OUTFLOW_TRAN_AMT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT'])]['OUTFLOW_TRAN_AMT_HKD'].max(),
       'TTL_TRAN_CNT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & ((x['OUTFLOW_TRAN_AMT_HKD'] > 0) | (x['INFLOW_TRAN_AMT_HKD'] > 0))]['TRAN_DT'].count(),
       'TTL_TRAN_CNT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & ((x['OUTFLOW_TRAN_AMT_HKD'] > 0) | (x['INFLOW_TRAN_AMT_HKD'] > 0))]['TRAN_DT'].count(),
       'TTL_TRAN_CNT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & ((x['OUTFLOW_TRAN_AMT_HKD'] > 0) | (x['INFLOW_TRAN_AMT_HKD'] > 0))]['TRAN_DT'].count(),
       'TTL_TRAN_CNT_M4':x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & ((x['OUTFLOW_TRAN_AMT_HKD'] > 0) | (x['INFLOW_TRAN_AMT_HKD'] > 0))]['TRAN_DT'].count(),
       'TTL_TRAN_CNT_M5':x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & ((x['OUTFLOW_TRAN_AMT_HKD'] > 0) | (x['INFLOW_TRAN_AMT_HKD'] > 0))]['TRAN_DT'].count(),
       'TTL_TRAN_CNT_M6':x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & ((x['OUTFLOW_TRAN_AMT_HKD'] > 0) | (x['INFLOW_TRAN_AMT_HKD'] > 0))]['TRAN_DT'].count(),
       'LAST_TRAN_DT':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0)]['TRAN_DT'].max(),
       'OUTLIER_INFLOW_TRAN_CNT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > MEAN_INFLOW_TRAN_AMT_HKD+2.5*STD_INFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_INFLOW_TRAN_CNT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > MEAN_INFLOW_TRAN_AMT_HKD+2.5*STD_INFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_INFLOW_TRAN_CNT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > MEAN_INFLOW_TRAN_AMT_HKD+2.5*STD_INFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_INFLOW_TRAN_CNT_M4':x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > MEAN_INFLOW_TRAN_AMT_HKD+2.5*STD_INFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_INFLOW_TRAN_CNT_M5':x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > MEAN_INFLOW_TRAN_AMT_HKD+2.5*STD_INFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_INFLOW_TRAN_CNT_M6':x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > MEAN_INFLOW_TRAN_AMT_HKD+2.5*STD_INFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_OUTFLOW_TRAN_CNT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > MEAN_OUTFLOW_TRAN_AMT_HKD+2.5*STD_OUTFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_OUTFLOW_TRAN_CNT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > MEAN_OUTFLOW_TRAN_AMT_HKD+2.5*STD_OUTFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_OUTFLOW_TRAN_CNT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > MEAN_OUTFLOW_TRAN_AMT_HKD+2.5*STD_OUTFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_OUTFLOW_TRAN_CNT_M4':x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > MEAN_OUTFLOW_TRAN_AMT_HKD+2.5*STD_OUTFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_OUTFLOW_TRAN_CNT_M5':x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > MEAN_OUTFLOW_TRAN_AMT_HKD+2.5*STD_OUTFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'OUTLIER_OUTFLOW_TRAN_CNT_M6':x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > MEAN_OUTFLOW_TRAN_AMT_HKD+2.5*STD_OUTFLOW_TRAN_AMT_HKD)]['TRAN_DT'].count(),
       'RECUR_INFLOW_TRAN_AMT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_INFLOW_TRAN_AMT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_INFLOW_TRAN_AMT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_INFLOW_TRAN_AMT_M4':x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_INFLOW_TRAN_AMT_M5':x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_INFLOW_TRAN_AMT_M6':x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['INFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_AMT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_AMT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_AMT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_AMT_M4':x[(x['TRAN_DT'] <= x['M4_END_DT']) & (x['TRAN_DT'] >= x['M4_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_AMT_M5':x[(x['TRAN_DT'] <= x['M5_END_DT']) & (x['TRAN_DT'] >= x['M5_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_AMT_M6':x[(x['TRAN_DT'] <= x['M6_END_DT']) & (x['TRAN_DT'] >= x['M6_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['OUTFLOW_TRAN_AMT_HKD'].sum(),
       'RECUR_OUTFLOW_TRAN_CNT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['TRAN_DT'].count(),
       'RECUR_OUTFLOW_TRAN_CNT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['TRAN_DT'].count(),
       'RECUR_OUTFLOW_TRAN_CNT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['OUTFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_OUTFLOW_TRAN_FLG'] == 1)]['TRAN_DT'].count(),
       'RECUR_INFLOW_TRAN_CNT_M1':x[(x['TRAN_DT'] <= x['M1_END_DT']) & (x['TRAN_DT'] >= x['M1_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['TRAN_DT'].count(),
       'RECUR_INFLOW_TRAN_CNT_M2':x[(x['TRAN_DT'] <= x['M2_END_DT']) & (x['TRAN_DT'] >= x['M2_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['TRAN_DT'].count(),
       'RECUR_INFLOW_TRAN_CNT_M3':x[(x['TRAN_DT'] <= x['M3_END_DT']) & (x['TRAN_DT'] >= x['M3_START_DT']) & (x['INFLOW_TRAN_AMT_HKD'] > 0) & (x['RECURRENT_INFLOW_TRAN_FLG'] == 1)]['TRAN_DT'].count()
    
}
        
   return pd.Series(names, index=['TTL_REV_AMT_M1','TTL_REV_AMT_M2','TTL_REV_AMT_M3','TTL_REV_AMT_M4','TTL_REV_AMT_M5','TTL_REV_AMT_M6','TTL_OUTFLOW_AMT_M1','TTL_OUTFLOW_AMT_M2','TTL_OUTFLOW_AMT_M3','TTL_OUTFLOW_AMT_M4',                    'TTL_OUTFLOW_AMT_M5','TTL_OUTFLOW_AMT_M6','TTL_OUTFLOW_CNT_M1','TTL_OUTFLOW_CNT_M2','TTL_OUTFLOW_CNT_M3',                    'TTL_OUTFLOW_CNT_M4','TTL_OUTFLOW_CNT_M5','TTL_OUTFLOW_CNT_M6','TTL_INFLOW_AMT_M1','TTL_INFLOW_AMT_M2',                    'TTL_INFLOW_AMT_M3','TTL_INFLOW_AMT_M4','TTL_INFLOW_AMT_M5','TTL_INFLOW_AMT_M6','TTL_INFLOW_CNT_M1',                    'TTL_INFLOW_CNT_M2','TTL_INFLOW_CNT_M3','TTL_INFLOW_CNT_M4','TTL_INFLOW_CNT_M5','TTL_INFLOW_CNT_M6',                    'MAX_INFLOW_TRAN_AMT_M1','MAX_OUTFLOW_TRAN_AMT_M1','TTL_TRAN_CNT_M1','TTL_TRAN_CNT_M2','TTL_TRAN_CNT_M3',                    'TTL_TRAN_CNT_M4','TTL_TRAN_CNT_M5','TTL_TRAN_CNT_M6','LAST_TRAN_DT','OUTLIER_INFLOW_TRAN_CNT_M1',                    'OUTLIER_INFLOW_TRAN_CNT_M2','OUTLIER_INFLOW_TRAN_CNT_M3','OUTLIER_INFLOW_TRAN_CNT_M4','OUTLIER_INFLOW_TRAN_CNT_M5',                    'OUTLIER_INFLOW_TRAN_CNT_M6','OUTLIER_OUTFLOW_TRAN_CNT_M1','OUTLIER_OUTFLOW_TRAN_CNT_M2','OUTLIER_OUTFLOW_TRAN_CNT_M3',                    'OUTLIER_OUTFLOW_TRAN_CNT_M4','OUTLIER_OUTFLOW_TRAN_CNT_M5','OUTLIER_OUTFLOW_TRAN_CNT_M6','RECUR_INFLOW_TRAN_AMT_M1',                    'RECUR_INFLOW_TRAN_AMT_M2','RECUR_INFLOW_TRAN_AMT_M3','RECUR_INFLOW_TRAN_AMT_M4','RECUR_INFLOW_TRAN_AMT_M5','RECUR_INFLOW_TRAN_AMT_M6',                    'RECUR_OUTFLOW_TRAN_AMT_M1','RECUR_OUTFLOW_TRAN_AMT_M2','RECUR_OUTFLOW_TRAN_AMT_M3','RECUR_OUTFLOW_TRAN_AMT_M4',                    'RECUR_OUTFLOW_TRAN_AMT_M5','RECUR_OUTFLOW_TRAN_AMT_M6','RECUR_OUTFLOW_TRAN_CNT_M1','RECUR_OUTFLOW_TRAN_CNT_M2','RECUR_OUTFLOW_TRAN_CNT_M3',                    'RECUR_INFLOW_TRAN_CNT_M1','RECUR_INFLOW_TRAN_CNT_M2','RECUR_INFLOW_TRAN_CNT_M3'])


# In[21]:


df_MONTHLY_TRAN_SMRY = df_DAILY_BS_TRAN_CA.groupby(['ACCT_ID']).apply(MONTHLY_TRAN_SMRY)


# In[22]:


#Creating Inflow / Outflow Transaction Flag
#Def Condition Functions
#Function Name: TRAN_INFLOW_OUTFLOW_FLG
#Function Description: This function generates inflow / outflow transaction flags for each date
def TRAN_INFLOW_OUTFLOW_FLG(x):
   names = {
       'DAILY_INFLOW_FLG': x[(x['INFLOW_TRAN_AMT_HKD'] > 0)]['TRAN_DT'].count(),
       'DAILY_OUTFLOW_FLG': x[(x['OUTFLOW_TRAN_AMT_HKD'] > 0)]['TRAN_DT'].count()
}
        
   return pd.Series(names, index=['DAILY_INFLOW_FLG','DAILY_OUTFLOW_FLG'])


# In[23]:


df_TRAN_FLG = df_DAILY_BS_TRAN_CA.groupby(['ACCT_ID','TRAN_DT']).apply(TRAN_INFLOW_OUTFLOW_FLG)


# In[24]:


df_TRAN_FLG.head()


# In[25]:


#Creating DAY-END BALANCE related variable
bal_date_rng = pd.to_datetime(df_DAILY_BS_ACCT['ACCT_BAL_DT'], format = '%d/%m/%Y')
df_DAILY_BS_ACCT['ACCT_BAL_DT'] = bal_date_rng
df_DAILY_BS_ACCT['ACCT_BAL_DT'].dtype


# In[26]:


#Filling in missing dates in the month-end balance table
df_DAILY_BS_ACCT = df_DAILY_BS_ACCT.set_index('ACCT_BAL_DT').resample('1D').first().fillna(0).reset_index()


# In[27]:


df_DAILY_BS_ACCT.head()


# In[28]:


#Creating Days without transactions related Variable
#Def Condition Functions
#Function Name: DAYS_WO_TRAN_SMRY
#Function Description: This function sets up the conditions for calculating the # of days without transactions
def DAYS_WO_TRAN_SMRY(x):
   names = {
       'DAYS_WO_INFLOW_TRAN_CNT_M1':x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT']) & (x['DAILY_INFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_INFLOW_TRAN_CNT_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT']) & (x['DAILY_INFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_INFLOW_TRAN_CNT_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT']) & (x['DAILY_INFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_INFLOW_TRAN_CNT_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT']) & (x['DAILY_INFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_INFLOW_TRAN_CNT_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT']) & (x['DAILY_INFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_INFLOW_TRAN_CNT_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT']) & (x['DAILY_INFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_OUTFLOW_TRAN_CNT_M1':x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT']) & (x['DAILY_OUTFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_OUTFLOW_TRAN_CNT_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT']) & (x['DAILY_OUTFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_OUTFLOW_TRAN_CNT_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT']) & (x['DAILY_OUTFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_OUTFLOW_TRAN_CNT_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT']) & (x['DAILY_OUTFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_OUTFLOW_TRAN_CNT_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT']) & (x['DAILY_OUTFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count(),
       'DAYS_WO_OUTFLOW_TRAN_CNT_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT']) & (x['DAILY_OUTFLOW_FLG'] == 0)]['ACCT_BAL_DT'].count()
   }
        
   return pd.Series(names, index=['DAYS_WO_INFLOW_TRAN_CNT_M1','DAYS_WO_INFLOW_TRAN_CNT_M2','DAYS_WO_INFLOW_TRAN_CNT_M3',                                 'DAYS_WO_INFLOW_TRAN_CNT_M4','DAYS_WO_INFLOW_TRAN_CNT_M5','DAYS_WO_INFLOW_TRAN_CNT_M6',                                 'DAYS_WO_OUTFLOW_TRAN_CNT_M1','DAYS_WO_OUTFLOW_TRAN_CNT_M2','DAYS_WO_OUTFLOW_TRAN_CNT_M3',                                 'DAYS_WO_OUTFLOW_TRAN_CNT_M4','DAYS_WO_OUTFLOW_TRAN_CNT_M5','DAYS_WO_OUTFLOW_TRAN_CNT_M6'])


# In[29]:


df_DAYS_WO_TRAN_STG = df_DAILY_BS_ACCT
df_DAYS_WO_TRAN_STG = df_DAYS_WO_TRAN_STG.reindex(columns=df_DAYS_WO_TRAN_STG.columns.tolist() + time_stamp_str)   # add empty cols
df_DAYS_WO_TRAN_STG[time_stamp_str] = time_stamp_val
#Convert the other string datetime to Pandas Datetime format for further calculation
df_DAYS_WO_TRAN_STG[time_stamp_str] = df_DAYS_WO_TRAN_STG[time_stamp_str].apply(pd.to_datetime, errors='coerce')


# In[30]:


for i in range(0, len(df_DAYS_WO_TRAN_STG)):
    if (df_DAYS_WO_TRAN_STG.CUST_ID[i] == 0):
        df_DAYS_WO_TRAN_STG.CUST_ID[i] = df_DAYS_WO_TRAN_STG.CUST_ID[i-1]
        df_DAYS_WO_TRAN_STG.CUST_NAME[i] = df_DAYS_WO_TRAN_STG.CUST_NAME[i-1]
        df_DAYS_WO_TRAN_STG.ACCT_ID[i] = df_DAYS_WO_TRAN_STG.ACCT_ID[i-1]
        df_DAYS_WO_TRAN_STG.ACCT_TYP[i] = df_DAYS_WO_TRAN_STG.ACCT_TYP[i-1]


# In[31]:


df_DAILY_BS_ACCT = df_DAILY_BS_ACCT.reindex(columns=df_DAILY_BS_ACCT.columns.tolist() + time_stamp_str)   # add empty cols
df_DAILY_BS_ACCT[time_stamp_str] = time_stamp_val
#Convert the other string datetime to Pandas Datetime format for further calculation
df_DAILY_BS_ACCT[time_stamp_str] = df_DAILY_BS_ACCT[time_stamp_str].apply(pd.to_datetime, errors='coerce')


# In[32]:


df_DAILY_BS_ACCT.head()


# In[33]:


#If there is a day without transaction, use previous day's account balance.
for i in range(0, len(df_DAILY_BS_ACCT)):
    if (df_DAILY_BS_ACCT.CUST_ID[i] == 0):
        df_DAILY_BS_ACCT.CUST_ID[i] = df_DAILY_BS_ACCT.CUST_ID[i-1]
        df_DAILY_BS_ACCT.CUST_NAME[i] = df_DAILY_BS_ACCT.CUST_NAME[i-1]
        df_DAILY_BS_ACCT.ACCT_ID[i] = df_DAILY_BS_ACCT.ACCT_ID[i-1]
        df_DAILY_BS_ACCT.ACCT_TYP[i] = df_DAILY_BS_ACCT.ACCT_TYP[i-1]
        df_DAILY_BS_ACCT.ACCT_BAL[i] = df_DAILY_BS_ACCT.ACCT_BAL[i-1]


# In[34]:


df_DAILY_BS_ACCT.head()


# In[35]:


df_TRAN_FLG_STG1 = pd.merge(df_DAILY_BS_ACCT,df_TRAN_FLG, left_on=['ACCT_ID','ACCT_BAL_DT'],right_on=['ACCT_ID','TRAN_DT'],how = 'left')


# In[36]:


df_TRAN_FLG_STG1.head()


# In[37]:


#Check if the merge has been correctly done
df_TRAN_FLG_STG1.shape


# In[38]:


#Fill in zeros for NaN records
df_TRAN_FLG_STG1['DAILY_INFLOW_FLG'] = df_TRAN_FLG_STG1['DAILY_INFLOW_FLG'].fillna(0)
df_TRAN_FLG_STG1['DAILY_OUTFLOW_FLG'] = df_TRAN_FLG_STG1['DAILY_OUTFLOW_FLG'].fillna(0)


# In[39]:


df_TRAN_FLG_STG1.head()


# In[40]:


df_TRAN_FLG_STG2 = df_TRAN_FLG_STG1.groupby(['ACCT_ID']).apply(DAYS_WO_TRAN_SMRY)
df_TRAN_FLG_STG2.head()


# In[41]:


#Creating Inflow Transaction Sequence
tran_seq_inflow = 0

def TRAN_INFLOW_SEQ_DAYS(x):
    global tran_seq_inflow
    if x == 0:
        tran_seq_inflow+=1
    else :
        tran_seq_inflow = 0 
    return tran_seq_inflow


# In[42]:


#Creating Inflow Transaction Sequence
tran_seq_outflow = 0

def TRAN_OUTFLOW_SEQ_DAYS(x):
    global tran_seq_outflow
    if x == 0:
        tran_seq_outflow+=1
    else :
        tran_seq_outflow = 0 
    return tran_seq_outflow


# In[43]:


df_TRAN_FLG_STG1['TRAN_INFLOW_SEQ_DAYS'] = df_TRAN_FLG_STG1['DAILY_INFLOW_FLG'].apply(TRAN_INFLOW_SEQ_DAYS)
df_TRAN_FLG_STG1['TRAN_OUTFLOW_SEQ_DAYS'] = df_TRAN_FLG_STG1['DAILY_OUTFLOW_FLG'].apply(TRAN_OUTFLOW_SEQ_DAYS)


# In[46]:


df_TRAN_FLG_STG1.to_csv('TRAN_FLG_STG1.csv',header=True)
df_TRAN_FLG_STG1


# In[47]:


#Creating DAY END BALANCE Related Variable
#Def Condition Functions
#Function Name: MONTHLY_BAL_SMRY
#Function Description: This function sets up the conditions for aggregating daily balance attributes for last 6 months
def MONTHLY_BAL_SMRY(x):
   names = {
       'TTL_DAILY_BAL_AMT_M1': x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT'])]['ACCT_BAL'].sum(),
       'MIN_BAL_AMT_M1': x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT'])]['ACCT_BAL'].min(),
       'MIN_BAL_AMT_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT'])]['ACCT_BAL'].min(),
       'MIN_BAL_AMT_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT'])]['ACCT_BAL'].min(),
       'MIN_BAL_AMT_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT'])]['ACCT_BAL'].min(),
       'MIN_BAL_AMT_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT'])]['ACCT_BAL'].min(),
       'MIN_BAL_AMT_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT'])]['ACCT_BAL'].min(),
       'NEG_BAL_DAYS_M1': x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT']) & (x['ACCT_BAL'] <= 0)]['ACCT_BAL_DT'].count(),
       'NEG_BAL_DAYS_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT']) & (x['ACCT_BAL'] <= 0)]['ACCT_BAL_DT'].count(),
       'NEG_BAL_DAYS_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT']) & (x['ACCT_BAL'] <= 0)]['ACCT_BAL_DT'].count(),
       'NEG_BAL_DAYS_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT']) & (x['ACCT_BAL'] <= 0)]['ACCT_BAL_DT'].count(),
       'NEG_BAL_DAYS_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT']) & (x['ACCT_BAL'] <= 0)]['ACCT_BAL_DT'].count(),
       'NEG_BAL_DAYS_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT']) & (x['ACCT_BAL'] <= 0)]['ACCT_BAL_DT'].count(),
       'DAILY_BAL_STD_M1': x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT'])]['ACCT_BAL'].std(),
       'DAILY_BAL_STD_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT'])]['ACCT_BAL'].std(),
       'DAILY_BAL_STD_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT'])]['ACCT_BAL'].std(),
       'DAILY_BAL_STD_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT'])]['ACCT_BAL'].std(),
       'DAILY_BAL_STD_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT'])]['ACCT_BAL'].std(),
       'DAILY_BAL_STD_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT'])]['ACCT_BAL'].std()
   }
        
   return pd.Series(names, index=['TTL_DAILY_BAL_AMT_M1','MIN_BAL_AMT_M1','MIN_BAL_AMT_M2',                                 'MIN_BAL_AMT_M3','MIN_BAL_AMT_M4','MIN_BAL_AMT_M5','MIN_BAL_AMT_M6',                                 'NEG_BAL_DAYS_M1','NEG_BAL_DAYS_M2','NEG_BAL_DAYS_M3','NEG_BAL_DAYS_M4','NEG_BAL_DAYS_M5',                                 'NEG_BAL_DAYS_M6','DAILY_BAL_STD_M1','DAILY_BAL_STD_M2','DAILY_BAL_STD_M3','DAILY_BAL_STD_M4',                                 'DAILY_BAL_STD_M5','DAILY_BAL_STD_M6'])


# In[48]:


df_MONTHLY_BAL_SMRY = df_DAILY_BS_ACCT.groupby(['ACCT_ID']).apply(MONTHLY_BAL_SMRY)


# In[49]:


df_MONTHLY_BAL_SMRY.head()


# In[50]:


#Def Condition Functions
#Function Name: MAX_SEQ_DAYS_WO_TRAN
#Function Description: This function sets up the conditions for aggregating daily balance attributes for last 6 months
def MAX_SEQ_DAYS_WO_TRAN(x):
   names = {
       'MAX_SEQ_DAYS_WO_INFLOW_M1': x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT'])]['TRAN_INFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_INFLOW_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT'])]['TRAN_INFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_INFLOW_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT'])]['TRAN_INFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_INFLOW_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT'])]['TRAN_INFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_INFLOW_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT'])]['TRAN_INFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_INFLOW_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT'])]['TRAN_INFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_OUTFLOW_M1': x[(x['ACCT_BAL_DT'] <= x['M1_END_DT']) & (x['ACCT_BAL_DT'] >= x['M1_START_DT'])]['TRAN_OUTFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_OUTFLOW_M2': x[(x['ACCT_BAL_DT'] <= x['M2_END_DT']) & (x['ACCT_BAL_DT'] >= x['M2_START_DT'])]['TRAN_OUTFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_OUTFLOW_M3': x[(x['ACCT_BAL_DT'] <= x['M3_END_DT']) & (x['ACCT_BAL_DT'] >= x['M3_START_DT'])]['TRAN_OUTFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_OUTFLOW_M4': x[(x['ACCT_BAL_DT'] <= x['M4_END_DT']) & (x['ACCT_BAL_DT'] >= x['M4_START_DT'])]['TRAN_OUTFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_OUTFLOW_M5': x[(x['ACCT_BAL_DT'] <= x['M5_END_DT']) & (x['ACCT_BAL_DT'] >= x['M5_START_DT'])]['TRAN_OUTFLOW_SEQ_DAYS'].max(),
       'MAX_SEQ_DAYS_WO_OUTFLOW_M6': x[(x['ACCT_BAL_DT'] <= x['M6_END_DT']) & (x['ACCT_BAL_DT'] >= x['M6_START_DT'])]['TRAN_OUTFLOW_SEQ_DAYS'].max()     
   }
        
   return pd.Series(names, index=['MAX_SEQ_DAYS_WO_INFLOW_M1','MAX_SEQ_DAYS_WO_INFLOW_M2','MAX_SEQ_DAYS_WO_INFLOW_M3',                                 'MAX_SEQ_DAYS_WO_INFLOW_M4','MAX_SEQ_DAYS_WO_INFLOW_M5','MAX_SEQ_DAYS_WO_INFLOW_M6',                                 'MAX_SEQ_DAYS_WO_OUTFLOW_M1','MAX_SEQ_DAYS_WO_OUTFLOW_M2','MAX_SEQ_DAYS_WO_OUTFLOW_M3',                                 'MAX_SEQ_DAYS_WO_OUTFLOW_M4','MAX_SEQ_DAYS_WO_OUTFLOW_M5','MAX_SEQ_DAYS_WO_OUTFLOW_M6'])


# In[51]:


df_TRAN_FLG_SMRY = df_TRAN_FLG_STG1.groupby(['ACCT_ID']).apply(MAX_SEQ_DAYS_WO_TRAN)


# In[52]:


df_TRAN_FLG_SMRY.head()


# In[53]:


df_ACCT_MAST_STG1 = df_ACCT_MAST_STG1.join(df_MONTHLY_BAL_SMRY, on='ACCT_ID')
df_ACCT_MAST_STG1 = df_ACCT_MAST_STG1.join(df_MONTHLY_TRAN_SMRY, on='ACCT_ID')
df_ACCT_MAST_STG1 = df_ACCT_MAST_STG1.join(df_TRAN_FLG_SMRY, on='ACCT_ID')
df_ACCT_MAST_STG1 = df_ACCT_MAST_STG1.join(df_TRAN_FLG_STG2, on='ACCT_ID')


# In[54]:


df_ACCT_MAST_STG1.head()


# In[56]:


df_ACCT_MAST_STG1.to_csv('BS_ACCT_SMRY.csv',header=True)


# In[57]:


#Creating Bank Statement Scorecard Attributes
df_ACCT_MAST_STG2 = df_ACCT_MAST_STG1
df_ACCT_MAST_STG2['Last 3m # of Seemingly Recurrent Inflow Sources'] = (df_ACCT_MAST_STG2['RECUR_INFLOW_TRAN_CNT_M1'] + df_ACCT_MAST_STG2['RECUR_INFLOW_TRAN_CNT_M2'] + df_ACCT_MAST_STG2['RECUR_INFLOW_TRAN_CNT_M3'])
df_ACCT_MAST_STG2['Last 3m # of Seemingly Recurrent Outflow Destinations'] = (df_ACCT_MAST_STG2['RECUR_OUTFLOW_TRAN_CNT_M1'] + df_ACCT_MAST_STG2['RECUR_OUTFLOW_TRAN_CNT_M2'] + df_ACCT_MAST_STG2['RECUR_OUTFLOW_TRAN_CNT_M3'])
df_ACCT_MAST_STG2['Last 3m % Of Seemingly Recurrent Inflow Transactions Amount'] = ((df_ACCT_MAST_STG2['RECUR_INFLOW_TRAN_AMT_M1'] + df_ACCT_MAST_STG2['RECUR_INFLOW_TRAN_AMT_M2'] + df_ACCT_MAST_STG2['RECUR_INFLOW_TRAN_AMT_M3'])/(df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M2'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M3']))*100
df_ACCT_MAST_STG2['Last 3m % Of Seemingly Recurrent Outflow Transactions Amount'] = ((df_ACCT_MAST_STG2['RECUR_OUTFLOW_TRAN_AMT_M1'] + df_ACCT_MAST_STG2['RECUR_OUTFLOW_TRAN_AMT_M2'] + df_ACCT_MAST_STG2['RECUR_OUTFLOW_TRAN_AMT_M3'])/(df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M2'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M3']))*100
df_ACCT_MAST_STG2['Last 3m Average % Of Inflow Transactions from Top 3 Clients'] = 30.00
df_ACCT_MAST_STG2['Last 3m Average % Of Outflow Transactions to Top 3 Expense Destinations'] = 40.00
df_ACCT_MAST_STG2['Last 3m Avg Revenue as % of Prev 3m Avg Revenue'] = ((df_ACCT_MAST_STG2['TTL_REV_AMT_M1'] + df_ACCT_MAST_STG2['TTL_REV_AMT_M2'] + df_ACCT_MAST_STG2['TTL_REV_AMT_M3'])/(df_ACCT_MAST_STG2['TTL_REV_AMT_M4'] + df_ACCT_MAST_STG2['TTL_REV_AMT_M5'] + df_ACCT_MAST_STG2['TTL_REV_AMT_M6']))*100
df_ACCT_MAST_STG2['Last 3m Max # Days Without Outflow Transactions'] = df_ACCT_MAST_STG2[['DAYS_WO_OUTFLOW_TRAN_CNT_M1','DAYS_WO_OUTFLOW_TRAN_CNT_M2','DAYS_WO_OUTFLOW_TRAN_CNT_M3']].max(axis=1)
df_ACCT_MAST_STG2['Last 3m Max Extra Large (Upper Outlier > 2.5*stddev) Inflow Count'] = df_ACCT_MAST_STG2[['OUTLIER_INFLOW_TRAN_CNT_M1','OUTLIER_INFLOW_TRAN_CNT_M2','OUTLIER_INFLOW_TRAN_CNT_M3']].max(axis=1)
df_ACCT_MAST_STG2['Last 3m Max Extra Large (Upper Outlier > 2.5*stddev) Outflow Count'] = df_ACCT_MAST_STG2[['OUTLIER_OUTFLOW_TRAN_CNT_M1','OUTLIER_OUTFLOW_TRAN_CNT_M2','OUTLIER_OUTFLOW_TRAN_CNT_M3']].max(axis=1)
df_ACCT_MAST_STG2['Last 3m Max Negative Balances Days Count'] = df_ACCT_MAST_STG2[['NEG_BAL_DAYS_M1','NEG_BAL_DAYS_M2','NEG_BAL_DAYS_M3']].max(axis=1)
df_ACCT_MAST_STG2['Last 3m Max Sequence Of Days Without Outflow Transactions'] = df_ACCT_MAST_STG2[['MAX_SEQ_DAYS_WO_OUTFLOW_M1','MAX_SEQ_DAYS_WO_OUTFLOW_M2','MAX_SEQ_DAYS_WO_OUTFLOW_M3']].max(axis=1)
df_ACCT_MAST_STG2['Last 3m Revenue Volatility as % of Prev 3m Revenue Volatility'] = (df_ACCT_MAST_STG2[['TTL_REV_AMT_M1','TTL_REV_AMT_M2','TTL_REV_AMT_M3']].std(axis=1)/df_ACCT_MAST_STG2[['TTL_REV_AMT_M4','TTL_REV_AMT_M5','TTL_REV_AMT_M6']].std(axis=1))*100
df_ACCT_MAST_STG2['Last 3m Total Inflow Count'] = df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M1'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M2'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M3']
df_ACCT_MAST_STG2['Last 3m Total Inflow Sum'] = df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M2'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M3']
df_ACCT_MAST_STG2['Last 3m Total Negative Balances Days Count'] = df_ACCT_MAST_STG2['NEG_BAL_DAYS_M1'] + df_ACCT_MAST_STG2['NEG_BAL_DAYS_M2'] + df_ACCT_MAST_STG2['NEG_BAL_DAYS_M3']
df_ACCT_MAST_STG2['Last 3m Total Outflow Count'] = df_ACCT_MAST_STG2['TTL_OUTFLOW_CNT_M1'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_CNT_M2'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_CNT_M3']
df_ACCT_MAST_STG2['Last 3m Total Outflow Sum'] = df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M2'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M3']
df_ACCT_MAST_STG2['Last 6m Lowest Minimum Balance'] = df_ACCT_MAST_STG2[['MIN_BAL_AMT_M1','MIN_BAL_AMT_M2','MIN_BAL_AMT_M3','MIN_BAL_AMT_M4','MIN_BAL_AMT_M5','MIN_BAL_AMT_M6']].min(axis=1)
df_ACCT_MAST_STG2['Last 6m Lowest Minimum Balance as % of Total Outflow Amount'] = df_ACCT_MAST_STG2[['MIN_BAL_AMT_M1','MIN_BAL_AMT_M2','MIN_BAL_AMT_M3','MIN_BAL_AMT_M4','MIN_BAL_AMT_M5','MIN_BAL_AMT_M6']].min(axis=1)/(df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M2'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M3'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M4'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M5'] + df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M6'])
df_ACCT_MAST_STG2['Last 6m Max # Days Without Inflow Transactions'] = df_ACCT_MAST_STG2[['DAYS_WO_INFLOW_TRAN_CNT_M1','DAYS_WO_INFLOW_TRAN_CNT_M2','DAYS_WO_INFLOW_TRAN_CNT_M3','DAYS_WO_INFLOW_TRAN_CNT_M4','DAYS_WO_INFLOW_TRAN_CNT_M5','DAYS_WO_INFLOW_TRAN_CNT_M6']].max(axis=1)
df_ACCT_MAST_STG2['Last 6m Max Sequence Of Days Without Inflow Transactions'] = df_ACCT_MAST_STG2[['MAX_SEQ_DAYS_WO_INFLOW_M1','MAX_SEQ_DAYS_WO_INFLOW_M2','MAX_SEQ_DAYS_WO_INFLOW_M3','MAX_SEQ_DAYS_WO_INFLOW_M4','MAX_SEQ_DAYS_WO_INFLOW_M5','MAX_SEQ_DAYS_WO_INFLOW_M6']].max(axis=1)
df_ACCT_MAST_STG2['Last month # of Days Since Last Inflow Transaction'] = (datetime.strptime(M1_end_dt, '%m/%d/%Y') - df_ACCT_MAST_STG2['LAST_TRAN_DT']).dt.days
df_ACCT_MAST_STG2['Last month Average Daily # Transactions'] = df_ACCT_MAST_STG2['TTL_TRAN_CNT_M1']/((datetime.strptime(M1_end_dt, '%m/%d/%Y') - datetime.strptime(M1_start_dt, '%m/%d/%Y')).days + 1)
df_ACCT_MAST_STG2['Last month Average Daily Balance'] = df_ACCT_MAST_STG2['TTL_DAILY_BAL_AMT_M1']/((datetime.strptime(M1_end_dt, '%m/%d/%Y') - datetime.strptime(M1_start_dt, '%m/%d/%Y')).days + 1)
df_ACCT_MAST_STG2['Last month Average Inflow'] = df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M1']/df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M1']
df_ACCT_MAST_STG2['Last month Average Outflow'] = df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M1']/df_ACCT_MAST_STG2['TTL_OUTFLOW_CNT_M1']
df_ACCT_MAST_STG2['Last month Average Transaction Amount'] = (df_ACCT_MAST_STG2['TTL_OUTFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M1']) /(df_ACCT_MAST_STG2['TTL_OUTFLOW_CNT_M1']+df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M1'])
df_ACCT_MAST_STG2['Last month Avg Daily Balance Volatility as % of Last 3m Avg Daily Balance Volatility'] = ((df_ACCT_MAST_STG2['DAILY_BAL_STD_M1'])/((df_ACCT_MAST_STG2['DAILY_BAL_STD_M1']+df_ACCT_MAST_STG2['DAILY_BAL_STD_M2']+df_ACCT_MAST_STG2['DAILY_BAL_STD_M3'])/3))*100

Last_6m_ttl_inflow_amount = df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M1'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M2'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M3'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M4'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M5'] + df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M6']
Last_6m_ttl_inflow_count = df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M1'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M2'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M3'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M4'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M5'] + df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M6']

df_ACCT_MAST_STG2['Last month Avg Inflow Amount as % of Last 6m Avg Inflow Amount'] = ((df_ACCT_MAST_STG2['TTL_INFLOW_AMT_M1']/df_ACCT_MAST_STG2['TTL_INFLOW_CNT_M1'])/(Last_6m_ttl_inflow_amount/Last_6m_ttl_inflow_count))*100
df_ACCT_MAST_STG2['Last month Max Inflow'] = df_ACCT_MAST_STG2['MAX_INFLOW_TRAN_AMT_M1']
df_ACCT_MAST_STG2['Last month Max Outflow'] = df_ACCT_MAST_STG2['MAX_OUTFLOW_TRAN_AMT_M1']


