#!/usr/bin/env python
# coding: utf-8

# ## BUSINESS PROBLEM

# In[1]:


#FLO, an online shoe store, wants to divide its customers into segments and determine marketing strategies according to these segments. 
#To this end, customers' behaviors will be defined and groups will be created based on clusters in these behaviors.


# ### DATASET

# In[2]:


# The data set consists of information obtained from the past shopping behavior of customers who made their last 
# purchases from Flo via OmniChannel (both online and offline shopping) in 2020 - 2021.


# Variables
# master_id: Unique customer number
# order_channel: Which channel of the shopping platform is used (Android, iOS, Desktop, Mobile)
# last_order_channel: The channel where the last purchase was made
# first_order_date: The date of the customer's first purchase
# last_order_date: The last shopping date of the customer
# last_order_date_online: The last shopping date of the customer on the online platform
# last_order_date_offline: The last shopping date of the customer on the offline platform
# order_num_total_ever_online: Total number of purchases made by the customer on the online platform
# order_num_total_ever_offline: Total number of purchases made by the customer offline
# customer_value_total_ever_offline: Total price paid by the customer for offline purchases
# customer_value_total_ever_online: Total price paid by the customer for online purchases
# interested_in_categories_12: List of categories the customer has shopped in the last 12 months


# ### DATA UNDERSTANDING

# In[3]:


import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_ = pd.read_csv("/Users/yasemincingoz/Desktop/crmAnalytics/FLOMusteriSegmentasyonu/flo_data_20k.csv")
df = df_.copy()
df.head()


# In[4]:


df.shape
#19945 rows and 12 columns


# In[5]:


df.columns


# In[6]:


df.describe().T


# In[7]:


df.isnull().sum()
#data set is clean


# #### STEP 1

# In[8]:


# Omnichannel shows that customers do shopping both inline and offline
# Create new variables for the total number of purchases and expenditures of each customer


# In[9]:


df["total_number_purchases"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["expenditures"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]


# #### STEP 2

# In[10]:


# Look at the data types. Change the data type expresing date to date.


# In[11]:


date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)


# #### STEP 3

# In[12]:


# Look at the distribution of the number of customers, total number of products purchased and total expenditures in shopping channels.


# In[13]:


df.groupby("order_channel").agg({"expenditures": "sum", "total_number_purchases":"sum", "master_id": "count"})


# #### STEP 4

# In[14]:


# List the top 10 customers who bring the most profits


# In[15]:


df.sort_values("expenditures", ascending=False)[:10]


# #### STEP 5
# 

# In[16]:


# List the top 10 customers who place the most orders


# In[17]:


df.sort_values("total_number_purchases", ascending = False)[:10]


# #### STEP 6

# In[18]:


# Functionalize the data preparation process.


# In[19]:


def data_prep(dataframe):
    dataframe["total_number_purchases"] =  dataframe["order_num_total_ever_online"] +  dataframe["order_num_total_ever_offline"]
    dataframe["expenditures"] =  dataframe["customer_value_total_ever_online"] +  dataframe["customer_value_total_ever_offline"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    return df


# In[20]:


#########################################


# ## CALCULATING RFM METRICS

# In[21]:


# RFM analysis is marketing analysis technique  to use date based on existing customer behavior to predict 
# how a new customer is likely to act in the future.

# KEY FACTORS:
    # Recency: the fact of being recent, of having occurred a relatively short time ago. 
            # How recently they've  made a purchase
    # Frequency: total number of purchase (How often they buy)
    # Monetary: amount of money, ralting to money(how much do they spend)


# In[22]:


df["last_order_date"].max()


# In[23]:


# The analysis date is 2 days after the date of the last purchase in the data set.
analysis_date = dt.datetime(2021, 6, 1)
type(analysis_date)


# ## CALCULATING RFM METRICS

# In[24]:


# Recency, Frequency, Moneratary

rfm = pd.DataFrame()
# Create empty DataFrame called 'rfm'

rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
#This part converts the Series of timedelta objects into a Series of integers representing the number of days. 
#The astype('timedelta64[D]') function is used to cast the timedelta objects to a specific time unit, 
#in this case, days ('D')

rfm["frequency"] = df["total_number_purchases"]
rfm["monetary"] = df["expenditures"]

rfm.head()


# ## CALCULATION RFM SCORE

# In[25]:


#Convert Recency, Frequency and Monetary metrics into scores between 1-5 with the help of qcut.
#Save these scores as recency_score, frequency_score and monetary_score.


# In[26]:


rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])

rfm.head()


# In[27]:


# Express recency_score and frequency_score as a single variable and save it as RF_SCORE.


# In[28]:


rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm["frequency_score"].astype(str))
rfm.head()


# In[29]:


# DEFINING RF SCORE AS A SEGMENT


# In[30]:


seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


# In[31]:


rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)
#The regex=True argument indicates that the keys in the seg_map dictionary should be treated as regular expressions.

rfm


# In[32]:


# Examine the recency, frequency and monetary averages of the segments.


# In[33]:


rfm[['segment','recency','frequency', 'monetary']].groupby("segment").agg(['mean', 'count'])


# In[34]:


# FLO is adding a new women's shoe brand.
# The product prices of the included brand are above general customer preferences.
# For this reason, it is desired to specifically contact customers with the profile that will be interested in the promotion of the brand and product sales.
# Customers who will be contacted specifically are champions, loyal_customers and people who shop in the female category. Save the ID numbers of these customers in the csv file.


# In[41]:


target_segments = rfm[rfm['segment'].isin(["champions", "loyal_customers"])]["customer_id"]

cust_ids = df[(df["master_id"].isin(target_segments)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("new_brand_target_customer_id.csv", index=False)
cust_ids.shape
cust_ids
#rfm


# In[36]:


##########################################


# In[37]:


#Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. 
#Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir alışveriş yapmayan 
#kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniyor. 
#Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz.


# In[42]:


target_categ_men_kid = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_categ_men_kid)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("sales_target_customer_ids.csv", index=False)

cust_ids.shape
cust_ids

