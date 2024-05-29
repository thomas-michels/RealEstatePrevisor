import streamlit as st
from app.components.sidebar import get_side_bar


st.set_page_config(
    page_title="Get Imóveis",
    page_icon="🗺️",
    initial_sidebar_state="expanded"
)

get_side_bar()

st.write("# Bem vindo a Get Imóveis")

st.write("""
         Aqui você pode visualizar com facilidade os imóveis de Blumenau e realizar buscar personalizadas.
         """)

st.divider()

st.write("""
Feito por Thomas Michels Rodrigues.
         
Contato via email thomasmichels.bnu@gmail.com.
""")
