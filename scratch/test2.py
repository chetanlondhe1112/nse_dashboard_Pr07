from io import BytesIO
import yfinance as yf

import requests
import pandas as pd

r = requests.get('https://docs.google.com/spreadsheets/d/1CyNVxagUlqxm1BhTC_w4kaDS2whiZx38uBJjzV2Aw6E/export?format=csv',timeout=20)
data = r.content
    
df = pd.read_csv(BytesIO(data), index_col=0)
print(df)

x=[x.split(":")[1]+str(".NS") for x in df['Symbol'].to_list()]
print(x)
# Specify the date range for which you want the historical data
start_date = '2023-07-01'
end_date = '2023-08-05'

data=pd.DataFrame()

# Fetch the historical data
for st in x:
  data2 = yf.download(st, start=start_date, end=end_date)
  df=pd.DataFrame(data2["Close"])
  df=df.reset_index()
  '''
  import plotly.express as px
  fig=px.line(df,x="Date",y="Close")
  fig'''
  df.columns=["Date",st]
  df=df.set_index("Date")
  data=pd.concat([data,df.T])

print(data)
data.to_csv("nifty50.csv")