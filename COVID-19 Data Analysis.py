#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


# In[2]:


files = os.listdir('/Users/haleigh/Desktop/Udemy Courses/Data Analysis Projects/COVID-19 Project/COVID-19 Files')


# In[3]:


# print the files and show what .csv we are working with
files


# In[4]:


def read_data(path, filename):
    return pd.read_csv(path+'/'+filename)


# In[6]:


path = '/Users/haleigh/Desktop/Udemy Courses/Data Analysis Projects/COVID-19 Project/COVID-19 Files'
world_data = read_data(path, 'worldometer_data.csv')


# In[7]:


world_data.head()


# In[8]:


day_wise = read_data(path, files[2])


# In[9]:


group_data = read_data(path, files[1])


# In[10]:


usa_data = read_data(path, files[4])


# In[11]:


province_data = read_data(path, files[3])


# In[13]:


# analysing trend of total cases, deaths, recovered, and active cases
world_data.columns


# In[14]:


import plotly.express as px


# In[16]:


columns =['TotalCases','TotalDeaths','TotalRecovered','ActiveCases']
for i in columns:
    # creating tree map
    fig = px.treemap(world_data.iloc[0:20], values = i, path = ['Country/Region'], title = 'Countries with respect to their {}'.format(i)) # first 20 rows
    fig.show()


# In[17]:


day_wise.head()


# In[18]:


day_wise.columns


# In[19]:


# what is the trend of confirmed deaths, recovered, and active cases?
px.line(day_wise, x='Date', y=['Confirmed','Deaths','Recovered','Active'], title = 'COVID Cases with respect to date', template = 'plotly_dark')


# In[22]:


# visualize population of tests done ratio
# create the dones feature using population % total number of tests
population_test_ratio = world_data['Population']/world_data['TotalTests'].iloc[0:20]


# In[23]:


fig = px.bar(world_data.iloc[0:20], x='Country/Region', y=population_test_ratio[0:20] ,color='Country/Region', title = 'Population to Tests Done Ratio')
fig.show()


# In[28]:


# top 20 countries most affected by COVID19
fig = px.bar(world_data.iloc[0:20], x='Country/Region', y=['Serious,Critical', 'TotalDeaths', 'TotalRecovered', 'ActiveCases', 'TotalCases'], title = 'Countries Most Affected by COVID19')
fig.show()


# In[29]:


# top 20 countries with maximum confirmed cases
fig = px.bar(world_data.iloc[0:20], y = 'Country/Region', x = 'TotalCases', color = 'TotalCases', text = 'TotalCases')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 Countries: Maximum Confirmed Cases')
fig.show()


# In[30]:


world_data.sort_values(by='TotalDeaths',ascending=False)


# In[32]:


# top 20 countries with maximum total deaths
fig = px.bar(world_data.sort_values(by='TotalDeaths',ascending=False)[0:20],y = 'Country/Region', x = 'TotalDeaths', color = 'TotalDeaths', text = 'TotalDeaths')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 Countries: Total Deaths')
fig.show()


# In[33]:


# top 20 countries with maximum active cases
fig = px.bar(world_data.sort_values(by='ActiveCases',ascending=False)[0:20],y = 'Country/Region', x = 'ActiveCases', color = 'ActiveCases', text = 'ActiveCases')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 Countries: Total Active Cases')
fig.show()


# In[34]:


# top 20 countries with maximum recovered cases
fig = px.bar(world_data.sort_values(by='TotalRecovered',ascending=False)[0:20],y = 'Country/Region', x = 'TotalRecovered', color = 'TotalRecovered', text = 'TotalRecovered')
fig.update_layout(template = 'plotly_dark', title_text = 'Top 20 Countries: Total Recovered Cases')
fig.show()


# In[36]:


# worst affected countries
labels = world_data[0:15]['Country/Region'].values
cases =['TotalCases','TotalDeaths','TotalRecovered','ActiveCases']
for i in cases:
    fig = px.pie(world_data[0:15], values = i, names = labels,hole = 0.2, title = "{} Most Affected Countries Recorded By WHO".format(i))
    fig.show()


# In[37]:


# deaths to confirmed ratio
deaths_to_confirmed = world_data['TotalDeaths']/world_data['TotalCases']
deaths_to_confirmed


# In[38]:


px.bar(world_data, x='Country/Region', y=deaths_to_confirmed, title='Death to Confirmed Ratio in Affected Countries')


# In[39]:


# deaths to recovered ratio
deaths_to_recovered = world_data['TotalDeaths']/world_data['TotalRecovered']
px.bar(world_data, x='Country/Region', y=deaths_to_recovered, title='Death to Recovered Ratio in Affected Countries')


# In[40]:


# serious to deaths ratio
serious_to_deaths = world_data['Serious,Critical']/world_data['TotalDeaths']


# In[41]:


px.bar(world_data, x='Country/Region', y=serious_to_deaths, title='Serious to Deaths Ratio in Affected Countries')


# In[42]:


# tests to confirmed ratio
tests_to_confirmed = world_data['TotalTests']/world_data['TotalCases']
px.bar(world_data, x='Country/Region', y=tests_to_confirmed, title='Tests to Confirmed Ratio in Affected Countries')


# In[43]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go


# In[51]:


# type in country to see visualization automated

def country_visualization(df, country):
    data = df[df['Country/Region'] == country]
    
    data2 = data.loc[:,['Date','Confirmed', 'Deaths', 'Recovered', 'Active']]
    
    fig = make_subplots(rows = 1, cols = 4, subplot_titles = ('confirmed','Active','Recovered','Deaths'))
    
    fig.add_trace(
    go.Scatter(name='Confirmed',x=data2['Date'], y=data2['Confirmed']), row = 1, col = 1
    )
    
    fig.add_trace(
    go.Scatter(name='Deaths',x=data2['Date'], y=data2['Deaths']), row = 1, col = 2
    )
    
    fig.add_trace(
    go.Scatter(name='Recovered',x=data2['Date'], y=data2['Recovered']),row = 1, col = 3
    )

    fig.add_trace(
    go.Scatter(name='Active',x=data2['Date'], y=data2['Active']), row = 1, col = 4
    )
    
    fig.update_layout(height=600, width = 800, title_text = 'Date vs. Recorded Cases of {}'.format(country), template = 'plotly_dark')
    fig.show()


# In[56]:


# enter any country below, using India, Brazil, and Germany as example
country_visualization(group_data, 'India')
country_visualization(group_data, 'Brazil')
country_visualization(group_data, 'Germany')

