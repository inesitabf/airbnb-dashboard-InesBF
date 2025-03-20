gimport streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
df = pd.read_csv("airbnb.csv")
st.title("Airbnb Dashboard - Ines Borrero")

#we create tabs
tab1, tab2, tab3 = st.tabs(["Data Exploration", "Advanced Analysis", "Price Simulator"])

#TAB 1: Data Exploration
with tab1:
    st.header("Airbnb Data Exploration in Madrid")

    #filters on the side
    st.sidebar.header("Filters")
    neighbourhood_group = st.sidebar.multiselect("Select a neighborhood group", df["neighbourhood_group"].unique(), default=df["neighbourhood_group"].unique())
    neighbourhood = st.sidebar.multiselect("Select a neighborhood", df["neighbourhood"].unique(), default=df["neighbourhood"].unique())
    room_type = st.sidebar.multiselect("Select a room type", df["room_type"].unique(), default=df["room_type"].unique())

    #filter the dataset based on the user's selections
    df_filtered = df[
        (df["neighbourhood_group"].isin(neighbourhood_group)) &
        (df["neighbourhood"].isin(neighbourhood)) &
        (df["room_type"].isin(room_type))
    ]

    #plot: room type vs number of reviews
    st.subheader("Room Type vs. Number of Reviews")
    fig1 = px.bar(df_filtered, x="room_type", y="number_of_reviews", color="room_type", title="Number of Reviews per Room Type")
    st.plotly_chart(fig1)

    # plot: price distribution by room type
    st.subheader("Price Distribution by Room Type")
    fig2 = px.box(df_filtered, x="room_type", y="price", title="Price per Room Type")
    st.plotly_chart(fig2)

#TAB 2: advanced analysis
with tab2:
    st.header("Advanced Analysis")

    col1, col2 = st.columns(2)

    with col1:
        #map of all the listings
        st.subheader("Listings Map")
        st.map(df_filtered.dropna(), latitude="latitude", longitude="longitude")

    with col2:
        #price distribution by neighborhood
        st.subheader("Price Distribution by Neighborhood")
        fig3 = px.box(df_filtered[df_filtered["price"] < 600], x="neighbourhood", y="price", title="Prices by Neighborhood")
        st.plotly_chart(fig3)

    #Top 10 hosts with the most listings
    st.subheader("Top 10 Hosts with Most Listings")
    df_host = df_filtered.groupby(["host_id", "host_name"]).size().reset_index()
    df_host["host"] = df_host["host_id"].astype(str) + " --- " + df_host["host_name"]
    df_top10_host = df_host.sort_values(by=0, ascending=False).head(10)
    fig4 = px.bar(df_top10_host, x=0, y="host", orientation='h', title="Top 10 Hosts")
    st.plotly_chart(fig4)

#TAB 3: Price simulator
with tab3:
    st.header("Airbnb Price Simulator")

    #user selections
    selected_neighbourhood = st.selectbox("Select a neighborhood", df["neighbourhood"].unique())
    selected_room_type = st.selectbox("Select a room type", df["room_type"].unique())
    nights = st.number_input("Number of nights", min_value=1, value=1)

    #sort the dataset for similar listings
    df_similar = df[(df["neighbourhood"] == selected_neighbourhood) & (df["room_type"] == selected_room_type)]

    if not df_similar.empty:
        avg_price = df_similar["price"].mean()
        min_price = df_similar["price"].min()
        max_price = df_similar["price"].max()

        st.subheader("Recommended Price Range")
        st.write(f"💰 **Average price:** {avg_price:.2f} € per night")
        st.write(f"📉 **Minimum price:** {min_price:.2f} € per night")
        st.write(f"📈 **Maximum price:** {max_price:.2f} € per night")
        st.write(f"🔢 **Estimated cost for {nights} nights:** {avg_price * nights:.2f} €")

    else:
        st.write("Not enough data available for this neighborhood and room type.")
