#!/usr/bin/env python
# coding: utf-8

# ## Querying the Warehouse

# <div style="background-color: #cce5ff; padding: 10px; border-radius: 5px;">
#     <strong>Notes:</strong>
#     Thanks to the comprehensive work completed during the ETL phases, queries can now be executed with ease, offering low latency and improved clarity, as demonstrated below.
# </div>

# In[ ]:


import duckdb
import os


# #### Querying - 2.5 Volume Spikes

# In[10]:


# Set S3 credentials (skip if public bucket)
duckdb.sql(f"""
SET s3_region='{os.environ["AWS_REGION"]}';
SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
""")

# Query directly from S3
df = duckdb.sql("""
SELECT *
FROM 's3://ucl-de/data/crypto_top_volume_spikes.parquet'
""").df()

print(df.head())


# #### Querying - 3.1 Daily Return

# In[11]:


# Set S3 credentials (skip if public bucket)
duckdb.sql(f"""
SET s3_region='{os.environ["AWS_REGION"]}';
SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
""")

# Query directly from S3
df = duckdb.sql("""
SELECT *
FROM 's3://ucl-de/data/crypto_daily_return.parquet'
""").df()

df.head()


# #### Querying - 4.1 Rolling 7-day volatility

# In[12]:


# Set S3 credentials (skip if public bucket)
duckdb.sql(f"""
SET s3_region='{os.environ["AWS_REGION"]}';
SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
""")

# Query directly from S3
df = duckdb.sql("""
SELECT *
FROM 's3://ucl-de/data/crypto_volatility.parquet'
""").df()

df.head()


# #### Querying - 8.2 Sentiment vs Daily Returns

# In[13]:


# Set S3 credentials (skip if public bucket)
duckdb.sql(f"""
SET s3_region='{os.environ["AWS_REGION"]}';
SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
""")

# Query directly from S3
df = duckdb.sql("""
SELECT *
FROM 's3://ucl-de/data/sentiment_vs_daily_return.parquet'
""").df()

df.head()


# #### Querying - 8.3 Days When Sentiment Was High but Prices Dropped

# In[14]:


# Set S3 credentials (skip if public bucket)
duckdb.sql(f"""
SET s3_region='{os.environ["AWS_REGION"]}';
SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
""")

# Query directly from S3
df = duckdb.sql("""
SELECT *
FROM 's3://ucl-de/data/sentiment_high_prices_low.parquet'
""").df()

df.head()


# #### Querying - 8.4 Days When Sentiment Was Low but Prices Rose

# In[15]:


# Set S3 credentials (skip if public bucket)
duckdb.sql(f"""
SET s3_region='{os.environ["AWS_REGION"]}';
SET s3_access_key_id='{os.environ["AWS_ACCESS_KEY_ID"]}';
SET s3_secret_access_key='{os.environ["AWS_SECRET_ACCESS_KEY"]}';
""")

# Query directly from S3
df = duckdb.sql("""
SELECT *
FROM 's3://ucl-de/data/sentiment_low_prices_high.parquet'
""").df()

df.head()

