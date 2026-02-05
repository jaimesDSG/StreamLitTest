#import
import streamlit as st
import pandas as pd
import plotly.express as px 
from pathlib import Path
import requests
import random

@st.cache_data
def download_data():
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    url = "https://storage.googleapis.com/schoolofdata-datasets/Data-Analysis.Data-Visualization/CO2_per_capita.csv"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    (DATA_DIR / "CO2_per_capita.csv").write_bytes(response.content)
    
    
def top_n_emitters(df, start_year=2008, end_year=2011, nb_displayed=10):
    
    co2_filtred_df = df[(df["Year"] >= start_year ) & ( df["Year"] <= end_year )] 
    co2_by_country_df = co2_filtred_df[["Country Name", "CO2 Per Capita (metric tons)"]]\
                    .groupby("Country Name", as_index=False).mean()
    
    top_co2_df = co2_by_country_df.sort_values("CO2 Per Capita (metric tons)", ascending=False)[:nb_displayed]
    fig = px.bar(top_co2_df, x="Country Name", y="CO2 Per Capita (metric tons)") 
    
    return fig

st.markdown(" # Ma web App ")

st.text(" Bienvenu ! 👋 ")
if st.button("Click to launch balloons !!!! Or maybe some snow if lucky ?"):
    if random.randint(0, 4096) == 1:
        st.snow()
    else:
        st.balloons()

co2_df = pd.read_csv('../data/CO2_per_capita.csv', delimiter=';') 
st.table(co2_df.head())

st.text(co2_df.describe())

nb_top = st.slider("Nombre de pays à afficher", min_value=1, max_value=20, value=10)
year_begin = st.select_slider("Choisis l'annee de debut"
                 ,options=co2_df["Year"].unique())
year_end = st.select_slider("Choisis l'annee de fin"
                 ,options=co2_df["Year"].unique())

co2_df_to_plot = co2_df.dropna().sort_values(by="Year")

plot =top_n_emitters(co2_df,
                     start_year=(year_begin if year_begin < year_end else year_end),
                     end_year=(year_end if year_end > year_begin else year_begin), 
                     nb_displayed=nb_top
                     )
st.plotly_chart(plot)

geo = px.scatter_geo(co2_df_to_plot.dropna(), locations="Country Code",
                    hover_name="Country Name", # column added to hover information
                    size="CO2 Per Capita (metric tons)", # size of markers
                    animation_frame = "Year",
                    projection="natural earth")

st.plotly_chart(geo)