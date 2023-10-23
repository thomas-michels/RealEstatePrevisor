import streamlit as st
import streamlit_pydantic as sp
from app.models import SellingProperty
import time

st.write("# Precifique seu imóvel")
st.write("Para precificar seu imovel será necessário algumas informações dele.")

data = sp.pydantic_form(key="Imovel", model=SellingProperty, submit_label="Precificar")

if data:
    st.json(data.json())

    with st.spinner("Precificando..."):
        time.sleep(2)

    st.balloons()
    st.success("Preço de 2500")
