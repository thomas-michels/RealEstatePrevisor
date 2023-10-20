import folium
import streamlit as st
import pandas as pd
import branca
from streamlit_folium import st_folium

st.title("Real Estate Map")

df = pd.read_csv("./193.csv", delimiter=";", quotechar="|", index_col="id")

def get_coordinates(df):
    coordinates = []
    key_index = {}

    for i, key in enumerate(df.keys()):
        key_index[key] = i

    for row in df.values:
        coordinates.append({
            "title": row[key_index.get("title")],
            "neighborhood_name": row[key_index.get("neighborhood_name")],
            "latitude": row[key_index.get("latitude")],
            "longitude": row[key_index.get("longitude")],
        })

    return coordinates

coordinates = get_coordinates(df)

map = folium.Map(location=[-26.878599, -49.079493], zoom_start=12)

groups = {}


for coordinate in coordinates[:250]:
    neighbor = coordinate["neighborhood_name"]
    if neighbor not in groups:
        groups[neighbor] = folium.FeatureGroup(neighbor).add_to(map)

    folium.Marker([coordinate["latitude"], coordinate["longitude"]], tooltip=coordinate["title"]).add_to(groups[neighbor])

folium.LayerControl().add_to(map)

output = st_folium(map, width=700, height=500, returned_objects=[])
