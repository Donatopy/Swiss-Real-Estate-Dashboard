# Swiss Real Estate Dashboard

## Overview

The **Swiss Real Estate Dashboard** is an interactive Streamlit application designed to provide insights into the Swiss property market. The dashboard leverages various visualizations to help users analyze house prices, types of houses, living space versus number of rooms, year built versus price, and the most and least expensive localities.

The data used for this dashboard is sourced from Kaggle. You can explore the dataset [here](https://www.kaggle.com/datasets/etiennekaiser/switzerland-house-price-prediction-data/data).

## Features

- **Price Distribution**: Histogram showing the distribution of house prices.
- **House Type Distribution**: Pie chart depicting the proportion of different house types.
- **Living Space vs. Number of Rooms**: Scatter plot showing the relationship between living space and the number of rooms.
- **Year Built vs. Price**: Scatter plot illustrating the relationship between the year a house was built and its price.
- **Top 5 Most Expensive Localities**: Bar chart displaying the top 5 most expensive localities based on average house prices.
- **Top 5 Cheapest Localities**: Bar chart showing the top 5 cheapest localities.

## Prerequisites

Before running the dashboard, ensure you have the following installed:

- Python 3.7 or later
- Streamlit
- Pandas
- Plotly
- SQLAlchemy
- Snowflake SQLAlchemy

You can install the required Python packages using pip:

```bash
pip install streamlit pandas plotly sqlalchemy snowflake-sqlalchemy
