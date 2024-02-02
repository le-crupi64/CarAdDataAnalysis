import streamlit as st
import pandas as pd 
import plotly.express as px 
import matplotlib.pyplot as plt

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
# Replace null values in the odometer column with the yearly average
# Group by 'model_year' and calculate the average for 'odometer'
grouped_average = df.groupby('model_year')['odometer'].transform('mean')
# Use the grouped average to fill missing values in 'column_to_fill'
df['odometer'] = df['odometer'].fillna(grouped_average)
# Drop rows with null values in the model year or odometer columns 
df= df.dropna(axis='rows')

# Add in Header 
st.header('Car Listing Data Analysis')

# FIG 1: Vehicles Listed by make Chart 

fig1 =px.histogram(df, x="make", title=' Number of Vehicles Listed by Make')
fig1.update_layout(xaxis_title='Vehicle Make ', yaxis_title='Number of Vehicles Listed')
st.plotly_chart(fig1)

st.write('The majority of vehicles listed are made by Ford (12.6k) followed by Chevrolet (10.61k) and Toyota (5.4k). Mercedes has the least number of vehicles listed (41).')


# FIG 2: model year by price with make Chart
fig2 = px.scatter(df, x="model_year", y="price", color='make', title="Price vs. Model Year")
fig2.update_layout(xaxis_title='Model Year', yaxis_title='Price')

st.plotly_chart(fig2)
st.write('There is a trend suggesting that the price of newer cars typicaly has a higher ceiling. I can also see an that Chevys and Fords from the 1960s are an exception to that trend. ')

# FIG 3: Price by Miles with Condition Selecter 
# Create a choice box to filter by car model
conditions = df["condition"].unique().tolist()
selected_conditions = st.selectbox("Choose a condition:", conditions)

# Filter the dataframe based on the selected car model
filtered_df = df[df["condition"] == selected_conditions]

price = filtered_df['price']
miles = filtered_df['odometer']

# Plot the price distribution
fig, ax = plt.subplots()
ax.scatter(miles, price)
plt.xlabel("Miles")
plt.ylabel("Price")
plt.title("Price Vs. Miles for " + selected_conditions)
plt.show()
# Display the plot in the Streamlit app
st.pyplot(plt)
st.write('We Can see that typically the lowest priced cars are salvage. Most cars listed are good, excellent, or like new. ')


# FIG 4: Price by Miles with Scale Switcher
st.title('Price Plot with Scale Switcher')
# Checkbox to switch between linear and logarithmic scale
log_scale = st.checkbox('Logarithmic Scale')
# Create a Plotly figure
x = df['odometer']
y = df['price']
fig4 = px.line(x=x, y=y, labels={'x': 'Odometer', 'y': 'Price'})

# Update y-axis scale based on the checkbox value
if log_scale:
    fig4.update_layout(yaxis_type='log')
else:
    fig4.update_layout(yaxis_type='linear')

# Display the Plotly figure using the Streamlit Plotly chart function
st.plotly_chart(fig4)

# FIG 5: Price Odometer and days listed compared
# Scatter Matrix with Filters 
# Dropdown for selecting dimensions
selected_dimensions = st.multiselect(
    'Select Dimensions:',
    ['odometer', 'days_listed', 'price'], 
    default=['price', 'days_listed']
)
# Scatter matrix plot
scatter_matrix = px.scatter_matrix(
    df,
    dimensions=selected_dimensions,
)
# Display the plot
st.plotly_chart(scatter_matrix)
st.write('As the miles on the car increases, the price decreases regardless of other factors.')

# Show conclusion 
st.header('Conclusions')
st.write('The majority of vehicles listed are made by Ford (12.6k) followed by Chevrolet (10.61k) and Toyota (5.4k). Mercedes has the least number of vehicles listed (41). There is a trend suggesting that the price of newer cars typicaly has a higher ceiling. I can also see an that Chevys and Fords from the 1960s are an exception to that trend.')