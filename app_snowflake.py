import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
# Configura la conexión a Snowflake usando los secretos
def get_engine():
    try:
        # Obtener secretos
        config = st.secrets["snowflake"]
        st.write("Secretos cargados:", config)  # Verifica que los secretos se cargan correctamente
        
        # Crear la URL de conexión
        engine_url = (
            f'snowflake://{config["user"]}:{config["password"]}@{config["account"]}/'
            f'{config["database"]}/{config["schema"]}?warehouse={config["warehouse"]}'
        )
        st.write("Engine URL:", engine_url)  # Verifica la URL de conexión
        
        # Crear el motor de SQLAlchemy
        engine = create_engine(engine_url, echo=True)
        st.write("Engine creado con éxito.")
        return engine
    except KeyError as e:
        st.error(f"Error con los secretos: {e}")
        raise
    except Exception as e:
        st.error(f"Error al configurar la conexión: {e}")
        raise

def load_data():
    try:
        st.write("Intentando cargar datos...")
        engine = get_engine()  # Obtener el motor de conexión
        query = 'SELECT * FROM PROPERTY_DATA.HOUSES LIMIT 10;'
        st.write("Query SQL:", query)  # Verifica la consulta SQL
        
        # Ejecutar la consulta y cargar datos en un DataFrame
        with engine.connect() as conn:
            st.write("Conectando a Snowflake...")
            df = pd.read_sql(query, conn)
        
        st.write("Datos cargados con éxito.")
        st.write("Columnas del DataFrame:", df.columns)
        st.write("Primeras filas del DataFrame:", df.head())
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()
df = load_data()

# Rename columns to match expected names
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

# Convert PRICE column to numeric and handle missing values
df['PRICE'] = pd.to_numeric(df['PRICE'], errors='coerce').round(2)

# Filter out rows where PRICE is NaN or 0
df = df[df['PRICE'] > 0]

# Application Title
st.title("Swiss Real Estate Dashboard")

# Visualization: Price Distribution
st.subheader("Price Distribution")
fig1 = px.histogram(df, x="PRICE", nbins=20, title="Price Distribution")
fig1.update_layout(
    xaxis_title='Price (CHF)',
    yaxis_title='Count',
    xaxis_tickprefix='$',
    xaxis_tickformat='.2f'  # Format to two decimal places
)
st.plotly_chart(fig1)

# Visualization: House Type Distribution
st.subheader("House Type Distribution")
fig2 = px.pie(df, names='HOUSETYPE', title="House Type Distribution")
st.plotly_chart(fig2)

# Visualization: Living Space vs. Number of Rooms
st.subheader("Living Space vs. Number of Rooms")
fig3 = px.scatter(df, x="LIVINGSPACE", y="NUMBERROOMS",
                  title="Living Space vs. Number of Rooms",
                  labels={"LIVINGSPACE": "Living Space (m²)", "NUMBERROOMS": "Number of Rooms"})
st.plotly_chart(fig3)

# Visualization: Year Built vs. Price
st.subheader("Year Built vs. Price")
fig4 = px.scatter(df, x="YEARBUILT", y="PRICE",
                  title="Year Built vs. Price",
                  labels={"YEARBUILT": "Year Built", "PRICE": "Price (CHF)"})
st.plotly_chart(fig4)

# Visualization: Top 5 Most Expensive Localities
st.subheader("Top 5 Most Expensive Localities")

# Calculate mean prices for each locality and round to 2 decimal places
mean_prices = df.groupby('LOCALITY')['PRICE'].mean().dropna().round(2)

# Get the top 5 most expensive localities
top_5_expensive = mean_prices.nlargest(5).reset_index()

# Plot the top 5 most expensive localities with warmer colors
fig5 = px.bar(top_5_expensive, x='LOCALITY', y='PRICE', color='LOCALITY',
              title='Top 5 Most Expensive Localities',
              labels={'PRICE': 'Average Price (CHF)', 'LOCALITY': 'Locality'},
              text='PRICE',
              color_discrete_sequence=px.colors.sequential.Oranges)  # Warmer color palette
fig5.update_layout(xaxis_title='Locality', yaxis_title='Average Price (CHF)',
                   showlegend=False)
fig5.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig5)

# Visualization: Top 5 Cheapest Localities
st.subheader("Top 5 Cheapest Localities")

# Get the top 5 cheapest localities
top_5_cheap = mean_prices.nsmallest(5).reset_index()

# Plot the top 5 cheapest localities with cooler colors
fig6 = px.bar(top_5_cheap, x='LOCALITY', y='PRICE', color='LOCALITY',
              title='Top 5 Cheapest Localities',
              labels={'PRICE': 'Average Price (CHF)', 'LOCALITY': 'Locality'},
              text='PRICE',
              color_discrete_sequence=px.colors.sequential.Blues)  # Cooler color palette
fig6.update_layout(xaxis_title='Locality', yaxis_title='Average Price (CHF)',
                   showlegend=False)
fig6.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig6)
