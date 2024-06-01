import streamlit as st
from app.components.sidebar import get_side_bar


st.set_page_config(
    page_title="Get Imóveis",
    page_icon="🗺️",
    initial_sidebar_state="expanded"
)

get_side_bar(current_path="listagem de imoveis")


st.write("Em breve!")
