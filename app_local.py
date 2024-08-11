import pandas as pd
import streamlit as st
import plotly.express as px

# Load the local dataset
df = pd.read_csv('cleaned_house_price_switzerland.csv')

# Convert Price column to numeric and handle missing values
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').round(2)

# Filter out rows where Price is NaN or 0
df = df[df['Price'] > 0]

# Application Title
st.title("Swiss Real Estate Dashboard")

# Visualization: Price Distribution
st.subheader("Price Distribution")
fig1 = px.histogram(df, x="Price", nbins=20, title="Price Distribution")
fig1.update_layout(
    xaxis_title='Price (CHF)',
    yaxis_title='Count',
    xaxis_tickprefix='$',
    xaxis_tickformat='.2f'  # Format to two decimal places
)
st.plotly_chart(fig1)

# Visualization: Distribution by house type
st.subheader("House Type Distribution")
fig2 = px.pie(df, names='HouseType', title="House Type Distribution")
st.plotly_chart(fig2)

# Visualization: Living Space vs. Number of Rooms
st.subheader("Living Space vs. Number of Rooms")
fig3 = px.scatter(df, x="LivingSpace", y="NumberRooms",
                  title="Living Space vs. Number of Rooms",
                  labels={"LivingSpace": "Living Space (m²)", "NumberRooms": "Number of Rooms"})
st.plotly_chart(fig3)

# Visualization: Year Built vs. Price
st.subheader("Year Built vs. Price")
fig4 = px.scatter(df, x="YearBuilt", y="Price",
                  title="Year Built vs. Price",
                  labels={"YearBuilt": "Year Built", "Price": "Price (CHF)"})
st.plotly_chart(fig4)

# New Visualization: Top 5 Most Expensive Localities
st.subheader("Top 5 Most Expensive Localities")

# Calculate mean prices for each locality and round to 2 decimal places
mean_prices = df.groupby('Locality')['Price'].mean().dropna().round(2)

# Get the top 5 most expensive localities
top_5_expensive = mean_prices.nlargest(5).reset_index()

# Plot the top 5 most expensive localities with warmer colors
fig5 = px.bar(top_5_expensive, x='Locality', y='Price', color='Locality',
              title='Top 5 Most Expensive Localities',
              labels={'Price': 'Average Price (CHF)', 'Locality': 'Locality'},
              text='Price',
              color_discrete_sequence=px.colors.sequential.Oranges)  # Warmer color palette
fig5.update_layout(xaxis_title='Locality', yaxis_title='Average Price (CHF)',
                   showlegend=False)
fig5.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig5)

# New Visualization: Top 5 Cheapest Localities
st.subheader("Top 5 Cheapest Localities")

# Get the top 5 cheapest localities
top_5_cheap = mean_prices.nsmallest(5).reset_index()

# Plot the top 5 cheapest localities with cooler colors
fig6 = px.bar(top_5_cheap, x='Locality', y='Price', color='Locality',
              title='Top 5 Cheapest Localities',
              labels={'Price': 'Average Price (CHF)', 'Locality': 'Locality'},
              text='Price',
              color_discrete_sequence=px.colors.sequential.Blues)  # Cooler color palette
fig6.update_layout(xaxis_title='Locality', yaxis_title='Average Price (CHF)',
                   showlegend=False)
fig6.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig6)
