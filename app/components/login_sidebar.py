import streamlit as st
import streamlit_pydantic as sp
from app.models.login import Login

def get_login_form() -> Login:
    with st.sidebar.container():
        data = sp.pydantic_form(key="Login", model=Login, submit_label="Entrar", clear_on_submit=True)

    return data
