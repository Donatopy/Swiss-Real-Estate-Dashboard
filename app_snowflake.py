import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine

def get_secrets():
    """Retrieve Snowflake connection secrets."""
    config = st.secrets.get("snowflake", {})
    if not config:
        st.error("Secrets not loaded. Please check your secrets.toml file.")
    return config

def create_engine_url(config):
    """Create Snowflake SQLAlchemy engine URL."""
    return (
        f'snowflake://{config["user"]}:{config["password"]}@{config["account"]}/'
        f'{config["database"]}/{config["schema"]}?warehouse={config["warehouse"]}'
    )

def load_data(engine):
    """Load data from Snowflake into a pandas DataFrame."""
    query = 'SELECT * FROM PROPERTY_DATA.HOUSES;'
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """Preprocess the DataFrame for analysis."""
    df.rename(columns={
        'price': 'PRICE', 
        'housetype': 'HOUSETYPE', 
        'size': 'SIZE', 
        'lotsize': 'LOTSIZE', 
        'balcony': 'BALCONY', 
        'livingspace': 'LIVINGSPACE', 
        'numberrooms': 'NUMBERROOMS', 
        'yearbuilt': 'YEARBUILT', 
        'locality': 'LOCALITY', 
        'postalcode': 'POSTALCODE'
    }, inplace=True)

    df['PRICE'] = pd.to_numeric(df['PRICE'], errors='coerce').round(2)
    df = df[df['PRICE'] > 0]
    return df

def plot_price_distribution(df):
    """Plot the distribution of house prices."""
    fig = px.histogram(df, x="PRICE", nbins=20, title="Price Distribution")
    fig.update_layout(
        xaxis_title='Price (CHF)',
        yaxis_title='Count',
        xaxis_tickprefix='$',
        xaxis_tickformat='.2f'
    )
    # Add description
    fig.add_annotation(
        text="This histogram shows the distribution of house prices in CHF. It helps to understand the frequency of various price ranges.",
        xref="paper", yref="paper",
        x=0.5, y=-0.15,
        showarrow=False,
        font=dict(size=12, color="grey"),
        align="center"
    )
    fig.update_layout(title_x=0.5)  # Center title
    st.plotly_chart(fig)

def plot_house_type_distribution(df):
    """Plot the distribution of house types."""
    fig = px.pie(df, names='HOUSETYPE', title="House Type Distribution")
    st.plotly_chart(fig)

def plot_living_space_vs_rooms(df):
    """Plot Living Space vs. Number of Rooms."""
    fig = px.scatter(df, x="LIVINGSPACE", y="NUMBERROOMS",
                      title="Living Space vs. Number of Rooms",
                      labels={"LIVINGSPACE": "Living Space (m²)", "NUMBERROOMS": "Number of Rooms"})
    st.plotly_chart(fig)

def plot_year_built_vs_price(df):
    """Plot Year Built vs. Price."""
    fig = px.scatter(df, x="YEARBUILT", y="PRICE",
                      title="Year Built vs. Price",
                      labels={"YEARBUILT": "Year Built", "PRICE": "Price (CHF)"})
    st.plotly_chart(fig)

def plot_top_expensive_localities(df):
    """Plot the top 5 most expensive localities."""
    mean_prices = df.groupby('LOCALITY')['PRICE'].mean().dropna().round(2)
    top_5_expensive = mean_prices.nlargest(5).reset_index()

    fig = px.bar(top_5_expensive, x='LOCALITY', y='PRICE', color='LOCALITY',
                  title='Top 5 Most Expensive Localities',
                  labels={'PRICE': 'Average Price (CHF)', 'LOCALITY': 'Locality'},
                  text='PRICE',
                  color_discrete_sequence=px.colors.sequential.Oranges)
    fig.update_layout(xaxis_title='Locality', yaxis_title='Average Price (CHF)',
                       showlegend=False)
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

def plot_top_cheap_localities(df):
    """Plot the top 5 cheapest localities."""
    mean_prices = df.groupby('LOCALITY')['PRICE'].mean().dropna().round(2)
    top_5_cheap = mean_prices.nsmallest(5).reset_index()

    fig = px.bar(top_5_cheap, x='LOCALITY', y='PRICE', color='LOCALITY',
                  title='Top 5 Cheapest Localities',
                  labels={'PRICE': 'Average Price (CHF)', 'LOCALITY': 'Locality'},
                  text='PRICE',
                  color_discrete_sequence=px.colors.sequential.Blues)
    fig.update_layout(xaxis_title='Locality', yaxis_title='Average Price (CHF)',
                       showlegend=False)
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

def main():
    """Main function to run the Streamlit app."""
    st.title("Swiss Real Estate Dashboard")

    # Add general description with link
    st.markdown("""
    Welcome to the Swiss Real Estate Dashboard! This application provides insights into the Swiss property market through various visualizations. 
    Explore the distribution of house prices, types of houses, and the relationship between living space, number of rooms, and year built. 
    Additionally, view the most and least expensive localities to make informed real estate decisions.

    The dataset used for this dashboard is sourced from Kaggle. You can find the dataset [here](https://www.kaggle.com/datasets/etiennekaiser/switzerland-house-price-prediction-data/data).
    """)

    # Get configuration secrets
    config = get_secrets()
    if not config:
        return
    
    # Create the SQLAlchemy engine
    engine_url = create_engine_url(config)
    engine = create_engine(engine_url, echo=False)
    
    # Load and preprocess the data
    df = load_data(engine)
    if df is None:
        return
    
    df = preprocess_data(df)
    
    # Generate and display plots in the new order
    plot_house_type_distribution(df)  # Previously 2nd
    plot_living_space_vs_rooms(df)     # Previously 3rd
    plot_year_built_vs_price(df)       # Previously 4th
    plot_price_distribution(df)        # Moved to 4th position
    plot_top_expensive_localities(df)  # Previously 5th
    plot_top_cheap_localities(df)      # Previously 6th

if __name__ == "__main__":
    main()
