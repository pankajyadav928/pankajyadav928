#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#Graphing Function 
def make_graph(stock_data, revenue_data, stock):
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[3]:


tesla = yf.Ticker('TSLA')


# In[4]:


tesla_data = tesla.history(period="max")

tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[12]:


#Question 2: Use Webscraping to Extract Tesla Revenue Data

url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data = requests.get(url).text



# In[13]:


tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('Tesla Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[11]:


revenue = col[1].text.replace("$", "").replace(",", "")
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$", "").str.replace(",", "")
tesla_revenue


# In[14]:


tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].astype(bool)]
tesla_revenue.dropna(inplace=True)
tesla_revenue.tail()


# In[15]:


#Question 3: Use yfinance to Extract Stock Data

gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
gme_data.head()


# In[20]:


#Question 4: Use Webscraping to Extract GME Revenue Data
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data = requests.get(url).text

                


# In[23]:


soup = BeautifulSoup(html_data,"html5lib")


# In[ ]:


gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[24]:


gme_revenue.tail()


# In[25]:


#Question 5: Plot Tesla Stock Graph
make_graph(tesla_data[['Date','Close']], tesla_revenue, 'Tesla')


# In[26]:


#Question 6: Plot GameStop Stock Graph
make_graph(gme_data[['Date','Close']], gme_revenue, 'GameStop')


# In[ ]:




