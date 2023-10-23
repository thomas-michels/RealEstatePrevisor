import folium
import streamlit as st
from streamlit_folium import st_folium
import requests
from app.configs import get_environment

_env = get_environment()


def get_data():
    url = f"{_env.PROPERTIES_API_URL}/properties"
    params = {"page_size": 1000, "offset": 0}

    data = requests.get(url=url, params=params)

    data.raise_for_status()
    st.session_state["data"] = data.json()["data"]
    
    all_properties = {}

    for property in data.json()["data"]:
        all_properties[f'{float(property["latitude"])}-{float(property["longitude"])}'] = property
    
    st.session_state["properties"] = all_properties

if "data" not in st.session_state:
    get_data()

map = folium.Map(location=[-26.878599, -49.079493], zoom_start=12)

groups = {}

properties = st.session_state["data"]

for property in properties:
    neighbor = property["neighborhood_name"]
    if neighbor not in groups:
        groups[neighbor] = folium.FeatureGroup(neighbor).add_to(map)

    popup = folium.Popup(
        f"""
            <a href="{property["property_url"]}" target="_blank">{property["title"]}</a><br>
            <br>
            {property["description"]}<br>
            <br>
            """,
        max_width=250,
    )
    
    folium.Marker([property["latitude"], property["longitude"]], tooltip=property["title"]).add_to(groups[neighbor])

folium.LayerControl().add_to(map)

output = st_folium(map, width=700, height=500)

clicked_property = output["last_object_clicked"]

if clicked_property:
    cached_property = st.session_state["properties"].get(f'{float(clicked_property["lat"])}-{str(clicked_property["lng"])}')
    if cached_property:
        st.write(f"## _{cached_property['title'].upper()}_")
        st.image(cached_property["image_url"])
        st.write(f"#### __{cached_property['type'].upper()} - {cached_property['modality_name'].upper()}__")
        st.metric(label="Preço", value=f"R$ {cached_property['price']:,}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(label="Quartos", value=cached_property["rooms"])
        col2.metric(label="Banheiros", value=cached_property["bathrooms"])
        col3.metric(label="Garagens", value=cached_property["parking_space"])
        col4.metric(label="Tamanho em m²", value=cached_property["size"])
        st.write(f"Mais detalhes no [link]({cached_property['property_url']}).")
