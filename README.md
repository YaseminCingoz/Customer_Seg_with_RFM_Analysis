# Customer_Segmentation_with_RFM_Analysis

### RFM analysis is marketing analysis technique  to use date based on existing customer behavior to predict  how a new customer is likely to act in the future.
### KEY FACTORS:
    # Recency: How recently they've  made a purchase 
    # Frequency: total number of purchase (How often they buy)
    # Monetary: amount of money, ralting to money(how much do they spend)

### BUSINESS PROBLEM
* FLO, an online shoe store, wants to divide its customers into segments and determine marketing strategies according to these segments. 
* To this end, customers' behaviors will be defined and groups will be created based on clusters in these behaviors.

### DATASET
* The data set consists of information obtained from the past shopping behavior of customers who made their last purchases from Flo via OmniChannel (both online and offline shopping) in 2020 - 2021.

### Variables
master_id: Unique customer number
order_channel: Which channel of the shopping platform is used (Android, iOS, Desktop, Mobile)
last_order_channel: The channel where the last purchase was made
first_order_date: The date of the customer's first purchase
last_order_date: The last shopping date of the customer
last_order_date_online: The last shopping date of the customer on the online platform
last_order_date_offline: The last shopping date of the customer on the offline platform
order_num_total_ever_online: Total number of purchases made by the customer on the online platform
order_num_total_ever_offline: Total number of purchases made by the customer offline
customer_value_total_ever_offline: Total price paid by the customer for offline purchases
customer_value_total_ever_online: Total price paid by the customer for online purchases
interested_in_categories_12: List of categories the customer has shopped in the last 12 months


### STESPS
- Data Understanding
- Omnichannel shows that customers do shopping both inline and offline. Create new variables for the total number of purchases and expenditures of each customer.
- Look at the data types. Change the data type expresing date to date.
- Look at the distribution of the number of customers, total number of products purchased and total expenditures in shopping channels.
- List the top 10 customers who bring the most profits.
- List the top 10 customers who place the most orders.
- Calculating RFM Metrics
- Calculating RFM Score
- Defining RFM Score as a Segment
- Examine the recency, frequency and monetary averages of the segments.
- De




