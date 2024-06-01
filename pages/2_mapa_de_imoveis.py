import folium
import streamlit as st
from streamlit_folium import st_folium
from app.services import PropertySearch
from app.components.sidebar import get_side_bar


st.set_page_config(layout="wide")

get_side_bar(current_path="mapa de imoveis")

def get_data(
        page_size: int=500,
        offset: int=0,
        rooms: int=0,
        bathrooms: int=0,
        parking_space: int=0,
        size: int=0,
        zip_code: str=""):

    property_search = PropertySearch(token=st.session_state.get("token"))

    properties = property_search.find_similar_properties(
        page_size=page_size,
        offset=offset,
        rooms=rooms,
        bathrooms=bathrooms,
        parking_space=parking_space,
        size=size,
        zip_code=zip_code
    )

    if not isinstance(properties, str):
        st.session_state["data"] = properties
    
        all_properties = {}

        for property in st.session_state["data"]:
            all_properties[f'{float(property["latitude"])}-{float(property["longitude"])}'] = property
        
        st.session_state["properties"] = all_properties

    else:
        st.toast(properties, icon="🚨")

def apply_filter():
    get_data(
        rooms=rooms,
        bathrooms=bathrooms,
        parking_space=parking_space,
        size=size,
        zip_code=zip_code
    )

def load_map():
    map = folium.Map(
        location=[-26.878599, -49.079493],
        zoom_start=12
    )

    groups = {}

    properties = st.session_state.get("data")

    if not properties:
        st.toast("Serviço indisponivel", icon="🚨")
        return []

    for property in properties:
        neighbor = property["neighborhood_name"]
        if neighbor not in groups:
            groups[neighbor] = folium.FeatureGroup(neighbor).add_to(map)
        
        folium.Marker([property["latitude"], property["longitude"]], tooltip=property["title"]).add_to(groups[neighbor])

    folium.LayerControl().add_to(map)
    return map

if "data" not in st.session_state:
    get_data()
    load_map()

with st.expander(label="Filtros") as filter:
    rooms = st.number_input(label="Quantidade de quartos", min_value=0)
    bathrooms = st.number_input(label="Quantidade de banheiros", min_value=0)
    parking_space = st.number_input(label="Quantidade de garagens", min_value=0)
    size = st.number_input(label="Tamanho em m²", min_value=0)
    zip_code = st.number_input(label="CEP")

btn_search = st.button(label="Filtrar", on_click=apply_filter)

loaded_map = load_map()

if loaded_map:
    output = st_folium(loaded_map, height=700, width=800)

    clicked_property = output["last_object_clicked"]

    if clicked_property:
        cached_property = st.session_state["properties"].get(f'{float(clicked_property["lat"])}-{str(clicked_property["lng"])}')
        if cached_property:
            st.write(f"## _{cached_property['title'].upper()}_")
            st.image(cached_property["image_url"], width=700)
            st.write(f"#### __{cached_property['type'].upper()} - {cached_property['modality_name'].upper()}__")
            st.metric(label="Preço", value=f"R$ {cached_property['price']:,}")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(label="Quartos", value=cached_property["rooms"])
            col2.metric(label="Banheiros", value=cached_property["bathrooms"])
            col3.metric(label="Garagens", value=cached_property["parking_space"])
            col4.metric(label="Tamanho em m²", value=cached_property["size"])
            st.write(f"Mais detalhes no [link]({cached_property['property_url']}).")
