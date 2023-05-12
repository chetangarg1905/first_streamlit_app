import streamlit 
import pandas
import requests
import snowflake.connector
from urlib.error import URLError

streamlit.title('My Parents New Healthy Diner')
  
streamlit.header('Breakfast Menu')
streamlit.text('🥣omega 3 & blueberry oatmeal')
streamlit.text('🥗kale , spinach & Rocket smoothie')
streamlit.text('🐔 Hard-boiled free-range egg')
streamlit.text('🥑🍞Avocado  Toast')
streamlit.header('🍌🥭Build your own fruit smoothie🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header('Fruityvice Fruit Advice')
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# json normalize
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output table
streamlit.dataframe(fruityvice_normalized)

#dont run anything past here while we troubleshoot
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

#
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
