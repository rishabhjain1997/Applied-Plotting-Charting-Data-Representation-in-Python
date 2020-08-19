
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[15]:

import matplotlib.pyplot as plt
import mplleaflet
get_ipython().magic('matplotlib inline')
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[16]:

hashid = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89'
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/{}.csv'.format(hashid))
df["Date"] = pd.to_datetime(df["Date"])
#df = df[df["Date"] < '2015-01-01']
df.sort_values(by=['Date'])
#df[df['Date'] == '2015-02-19']
#df.groupby(['Date', 'Element']).Data_Value.agg(['min', 'max'])
agg_values = df.groupby(['Date']).Data_Value.agg(['min', 'max'])
#gg_values
#agg_values[(agg_values.index.month == 2) & (agg_values.index.day == 19)]


# In[17]:

# hashid = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89'
# df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/{}.csv'.format(hashid))
# df["Date"] = pd.to_datetime(df["Date"])
# df = df[df["Date"] < '2015-01-01']
# df.sort_values(by=['Date'])
# #df.groupby(['Date', 'Element']).Data_Value.agg(['min', 'max'])
# agg_values = df.groupby(['Date']).Data_Value.agg(['min', 'max'])
# #agg_values.set_index('Date')
# plt.plot(agg_values['min']/10, '-c', label = 'Minimum temperature',linewidth=1)
# plt.plot(agg_values['max']/10, '-b',label = 'Max temperature',linewidth=1, alpha = 0.5)
# figure = plt.gcf()
# figure.set_size_inches(18.5, 10.5, forward=True)
# plt.gca().fill_between(agg_values.index,  
#                        agg_values["min"]/10, agg_values["max"]/10, 
#                        facecolor='grey', 
#                        alpha=0.3)
# plt.gca().spines['right'].set_visible(False)
# plt.gca().spines['top'].set_visible(False)
# plt.xticks(alpha = 0.8) 
# plt.yticks(alpha = 0.8) 
# plt.legend(loc='best', frameon=False)
# plt.title('Change in temperature over the period 2005-2015 in Ann Arbor and surrounding areas')
# plt.ylabel('Temperature in \N{DEGREE SIGN}C')


# In[18]:

def get_prev_min(row):
    month = row.month
    day = row.day
    data = decade_data[(decade_data.index.month == month) & (decade_data.index.day == day)]
    return (data["min"].min())

def get_prev_max(row):
    month = row.month
    day = row.day
    data = decade_data[(decade_data.index.month == month) & (decade_data.index.day == day)]
    return (data["max"].max())


# In[19]:

hashid = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89'
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/{}.csv'.format(hashid))
df["Date"] = pd.to_datetime(df["Date"])
df.sort_values(by=['Date'])
decade_df = df[df["Date"] < '2015-01-01']
decade_data = decade_df.groupby(['Date']).Data_Value.agg(['min', 'max'])


# In[20]:

year_df = df[(df["Date"] >= '2015-01-01') & (df["Date"] < '2016-01-01')]
agg_values = year_df.groupby(['Date']).Data_Value.agg(['min', 'max'])
year_data = agg_values.reset_index()
year_data["prev_min"] = year_data["Date"].apply(get_prev_min)
year_data["prev_max"] = year_data["Date"].apply(get_prev_max)
year_data.set_index("Date", inplace = True)
min_data = year_data.where(year_data["min"] < year_data["prev_min"]).dropna()
max_data = year_data.where(year_data["max"] > year_data["prev_max"]).dropna()
#year_data


# In[22]:

plt.plot(year_data['prev_min']/10, '-c', label = 'Record low temperatures during 2005-2014',linewidth=1)
plt.plot(year_data['prev_max']/10, '-b',label = 'Record high temperatures during 2005-2014',linewidth=1, alpha = 0.5)
figure = plt.gcf()
figure.set_size_inches(18.5, 10.5, forward=True)
plt.gca().fill_between(year_data.index,  
                       year_data["prev_min"]/10, year_data["prev_max"]/10, 
                       facecolor='grey', 
                       alpha=0.3)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.xticks(alpha = 0.8) 
plt.yticks(alpha = 0.8) 

plt.title('2015 Record-braking temperatures in Ann Arbor and surrounding areas')
plt.ylabel('Temperature in \N{DEGREE SIGN}C')
plt.scatter(min_data.index, min_data["min"]/10, label = 'Record breaking min. temperature in 2015')
plt.scatter(max_data.index, max_data["max"]/10, label = 'Record breaking max. temperature in 2015')
plt.legend(loc='best', frameon=False)


# In[ ]:



