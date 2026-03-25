# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests  
import pandas as pd


# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write(f"Name on your smoothie will be: {name_on_order}")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5,
)

if ingredients:
    ingredients_string = ''
    for ingredient in ingredients:
        ingredients_string += ingredient + ' '
        st.subheader(f"Nutrition for: {ingredient}")
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + ingredient)  
        st_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)  
    #st.text(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
                       values ('""" + name_on_order + """','""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")
