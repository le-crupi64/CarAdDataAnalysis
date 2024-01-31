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
# Make Cylinders column an object data type and fill null values with 'unknown'
df['cylinders'] = df['cylinders'].fillna('unknown')
# For the is_4wd column, fill Null values with 0 
df['is_4wd'] = df['is_4wd'].fillna(0)
# For the paint_color column, fill Null values with 'unknown'
df['paint_color'] = df['paint_color'].fillna('unknown')
# Drop rows with null values in the model year or odometer columns 
df= df.dropna(axis='rows')

# Add in Header 
st.header('Car Listing Data Analysis')

# Plot the Vehicles Listed by make Chart 
fig1 =px.histogram(df, x="make", title=' Number of Vehicles Listed by Make')
fig1.update_layout(xaxis_title='Vehicle Make ', yaxis_title='Number of Vehicles Listed')
fig1.show()
st.write('The majority of vehicles listed are made by Ford (12.6k) followed by Chevrolet (10.61k) and Toyota (5.4k). Mercedes has the least number of vehicles listed (41).')


# Plot The model year by price with make Chart
# Checkbox for data normalization
normalize_data = st.checkbox("Normalize Data", value=False)
# Scatter plot
fig = px.scatter(df, x="model_year", y="price", color="make", title="Price vs. Model Year")
fig.update_layout(xaxis_title='Model Year', yaxis_title='Price')
# Normalize data if the checkbox is selected
if normalize_data:
    fig.update_traces(marker=dict(size=10 / df['price']))
# Update layout
fig.update_layout(xaxis_title='Model Year', yaxis_title='Price')
# Display the plot
st.plotly_chart(fig)
st.write('There is a trend suggesting that the price of newer cars typicaly has a higher ceiling. I can also see an that Chevys and Fords from the 1960s are an exception to that trend. ')

#plot and show model year by price with condition
fig3 = px.scatter(df, x="model_year", y="price", color="condition", title="Price vs. Model Year")
fig3.update_layout(xaxis_title='Model Year', yaxis_title='Price')
st.plotly_chart(fig3, use_container_width=True)
st.write('We Can see that typically the lowest priced cars are salvage. Most cars listed are good, excellent, or like new. ')

# Scatter Matrix with Filters 
# Dropdown for selecting dimensions
selected_dimensions = st.multiselect(
    'Select Dimensions:',
    ['odometer', 'days_listed', 'price'], 
    default=['price', 'odometer']
)
# Scatter matrix plot
scatter_matrix = px.scatter_matrix(
    df,
    dimensions=selected_dimensions,
    color="model",
    category_orders={"model": df["model"].unique()},
    width=800,
    height=800
)
# Display the plot
st.plotly_chart(scatter_matrix)
st.write('As the miles on the car increases, the price decreases reguardless of other factors.')

# Show conclusion 
st.header('Conclusions')
st.write('The majority of vehicles listed are made by Ford (12.6k) followed by Chevrolet (10.61k) and Toyota (5.4k). Mercedes has the least number of vehicles listed (41). There is a trend suggesting that the price of newer cars typicaly has a higher ceiling. I can also see an that Chevys and Fords from the 1960s are an exception to that trend.')