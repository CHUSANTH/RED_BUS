import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie #pip
import requests #pip 
import pymysql
import pandas as pd

#Connecting VS-CODE to mysql
myconnection=pymysql.connect(host='localhost',user='root',passwd='root',port=3306)
mycursor=myconnection.cursor()

#streamlit part 
with st.sidebar:
   selected=option_menu(   
    menu_title="Menu",
    options=['Home','Find buses'],
    menu_icon=["collection-play"],
    icons=["house-gear-fill","bus-front-fill"],
    styles = {
    "container": {"padding": "10px", "background-color": "#000000"},  # Corrected styles
    "icon": {"color": "orange", "font-size": "25px"},
    "nav-link": {
        "font-size": "25px",
        "text-align": "left",
        "margin": "0px",
        "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "green"}
    },
    default_index=0)
   
if selected=='Home':  
   st.title(":green[REDBUS DATA SCRAPING WITH SELENIUM & DYNSMIC FILTERING USING STREAMLIT]")
   st.markdown("### :green[DOMAIN :]")
   st.markdown(''' - :orange[Social Media] ''')
   with st.container():
      col1, col2 = st.columns(2)
      with col1:
         st.markdown("### :green[Skills Take Away :]")
         st.markdown('''
               - :orange[Python scripting]
               - :orange[Web Scraping using Selenium]   
               - :orange[Data Management using SQL]  
               - :orange[Streamlit]
               - :orange[Data Analysis/Filtering using Streamlit] ''') 
      with col2:
         url=requests.get("https://lottie.host/6b52b7b8-ac9e-44ae-8765-8b2975b4c011/l151PrWWpt.json")
         url_json=dict()
         if url.status_code==200:
            url_json= url.json()
         else:
            print('Error in the url')
         st_lottie(url_json,width=200,height=300)
   
   st.markdown("### :green[ABOUT:]")
   st.markdown('''
           An application aims to revolutionize the transportation industry by providing a comprehensive solution for 
           collecting, analyzing, and visualizing bus travel data. By utilizing :blue[**Selenium**] for web scraping, 
           this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and 
           seat availability. By :blue[**streamlining**] data collection and providing powerful tools for data-driven 
           decision-making, this project can significantly improve operational efficiency and strategic planning in the 
           transportation industry.
         ''')
   st.markdown("### FOR FUTHER REFERANCE [click here](https://docs.google.com/document/d/1lWJU0W7BQC2x3_wv5Wlu6l6nHUgobxgXaL4V8vFu3FQ/edit) :bus:")

   

if selected=='Find buses':  #Scrap
   with st.container():
      col1, col2 = st.columns(2)
      with col1:
         st.title(":green[Select Your Bus:]")
      with col2:
        #lottie animation 
         url=requests.get("https://lottie.host/845025ac-b4ac-4389-9302-0f530cfeef56/1SMKYjJTvp.json")
         url_json=dict()
         if url.status_code==200:
            url_json= url.json()
         else:
            print('Error in the url')
         st_lottie(url_json,width=200,height=300)

#state_name-input
   queary_1='''select distinct State from bus_table'''
   mycursor.execute("use Redbus_project")
   mycursor.execute(queary_1)
   myconnection.commit()
   fetch1=mycursor.fetchall()
   df_state_name=pd.DataFrame(fetch1,columns=["State"])
   state_name = st.selectbox(':orange[Select your State :]',df_state_name,index=None,placeholder="Select the state name") #1

#route_name-input
   queary_2=f'''select distinct Route_name from bus_table where State='{state_name}' '''
   mycursor.execute("use Redbus_project")
   mycursor.execute(queary_2)
   myconnection.commit()
   fetch2=mycursor.fetchall()
   df_route_name=pd.DataFrame(fetch2,columns=["Route_name"])
   route_name = st.selectbox(':orange[Select your travelling Route :]',df_route_name,index=None,placeholder="Select the route name") #2

#bus_type-input
   queary_3=f'''select Bus_type from bus_table where State='{state_name}'and Route_name='{route_name}' '''
   mycursor.execute("use Redbus_project")
   mycursor.execute(queary_3)
   myconnection.commit()
   fetch3=mycursor.fetchall()
   df_bus_type=pd.DataFrame(fetch3,columns=["Bus_type"])
   bus_type = st.selectbox(':orange[Select Bus Type :]',df_bus_type,index=None,placeholder="Select your bus type")#3

#bus_catagory-input   
   queary_4=f'''select distinct Bus_category from bus_table where State='{state_name}' and Route_name='{route_name}' and Bus_type='{bus_type}' '''
   mycursor.execute("use Redbus_project")
   mycursor.execute(queary_4)
   myconnection.commit()
   fetch4=mycursor.fetchall()
   df_bus_catagory=pd.DataFrame(fetch4,columns=["Bus_category"])
   bus_catagory = st.selectbox(':orange[Select Catagory :]',df_bus_catagory,index=None,placeholder="Select your bus catagory(government/private)")#4

#submit button-to show bus details in data frame    
   if st.button("Submit"):
      queary=f'''select Bus_name,Departure,Duration,Reaching_time,Price,Rating,Seats_available from bus_table where State='{state_name}' and Route_name='{route_name}' and Bus_type='{bus_type}' and Bus_category='{bus_catagory}' '''
      mycursor.execute("use Redbus_project")
      mycursor.execute(queary)
      myconnection.commit()
      fetch=mycursor.fetchall()
      df_bus=pd.DataFrame(fetch,columns=["Bus_name","Departure","Duration","Reaching_time","Price","Rating","Seats_available"])
      st.table(df_bus)

#route_link for more details:[In-case of any issue] 
      queary_0=f'''select distinct Bus_route_link from bus_table where Route_name='{route_name}' '''
      mycursor.execute("use Redbus_project")
      mycursor.execute(queary_0)
      myconnection.commit()
      fetch0=mycursor.fetchall()
      df_route_name_link=pd.DataFrame(fetch0,columns=["Bus_route_link"])
      st.markdown("### For Further more Details,please visit [REDBUS](df_route_name_link['Bus_route_link'][0])")
