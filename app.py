import streamlit as st
import pandas as pd 
import plotly.express as px 

# Read in the Data
df = pd.read_csv("vehicles_us.csv")

# Clean Up the Data 
# Separate make and model into 2 columns 
df[['make', 'model']] = df['model'].str.split(' ',n=1, expand=True)

# Make model_year and date_posted the datetime data type 
df['model_year'] = pd.to_datetime(df['model_year'], format='%Y', errors='coerce').dt.year
df['date_posted'] = pd.to_datetime(df['date_posted'], format= '%Y-%m-%d')

# Add in Header 
st.header('Car Listing Data Analysis')

# Plot the Vehicles Listed by make Chart 
fig1= px.histogram(df, x="make", title=' Number of Vehicles Listed by Make')
st.plotly_chart(fig1, use_container_width=True)

# Plot The model year by price with make Chart
fig2 = fig = px.scatter(df, x="model_year", y="price", color="make", title="Price vs. Model Year")
st.plotly_chart(fig2, use_container_width=True)

# Use the check box to allow users to switch color from make to condition
agree = st.checkbox('See above chart with condition instead of make')

# If check box selected, plot and show model year by price with condition
if agree:
    fig3 = px.scatter(df, x="model_year", y="price", color="condition", title="Price vs. Model Year")
    st.plotly_chart(fig3, use_container_width=True)


# Show conclusion 
st.header('Conclusions', divider='blue')
st.write('The majority of vehicles listed are made by Ford (12.6k) followed by Chevrolet (10.61k) and Toyota (5.4k). Mercedes has the least number of vehicles listed (41). There is a trend suggesting that the price of newer cars typicaly has a higher ceiling. I can also see an that Chevys and Fords from the 1960s are an exception to that trend.')