import pandas as pd
import yfinance as yf
import streamlit as st

demo_url="https://docs.google.com/spreadsheets/d/1CyNVxagUlqxm1BhTC_w4kaDS2whiZx38uBJjzV2Aw6E/export?format=csv"

def mmultiple_days_data(sheet_df=pd.DataFrame(),start=str, end=str, column_to_read=str, price_type=str):
    data=pd.DataFrame()
    x=[x.split(":")[1]+str(".NS") for x in sheet_df[column_to_read].to_list()]
    # Fetch the historical data
    for stx in x:
        st.info("collecting data of {}".format(stx))
        data2 = yf.download(stx, start=start, end=end)
        df=pd.DataFrame(data2[price_type])
        df=df.reset_index()
        df.columns=["Date",stx]
        df=df.set_index("Date")
        data=pd.concat([data,df.T])
    return data 

def read_sheet(url=str):
    print("Connecting to your sheet")
    df=pd.read_csv(f"{url}")
    print(df)
    return df

# Specify the date range for which you want the historical data
start_date = '2023-07-01'
end_date = '2023-08-05'

st.title("Nifty Price Log")
col=st.columns((10,1))
sheet_url=col[0].text_input("",placeholder="google sheet link",label_visibility="collapsed")

st.info("Demo link : {}".format(demo_url))
if "nifty_data" not in st.session_state:
    st.session_state["nifty_data"]=pd.DataFrame()

if col[1].button("Ok",use_container_width=True):

    #read sheet
    #try:
    with st.spinner("Collecting Data.."):
        sheet_data=read_sheet(sheet_url)
    
        if len(sheet_data):
            st.success("Sheet read successfull.")
            
            #try:
            st.session_state["nifty_data"]=mmultiple_days_data(sheet_df=sheet_data,start=start_date,end=end_date,column_to_read="Symbol",price_type="Close")
            st.experimental_rerun()
            #except Exception as e:
                
            #    st.error("Collecting Data Failed..")
            #    st.error(e)
    #except Exception as e:
    #    st.error(e)
    #    st.error("Please, make sure your sheet is online?",icon="⚠️")

st.subheader("Nifty Data") 
st.dataframe(st.session_state["nifty_data"],use_container_width=True)      
                