import streamlit as st
import streamlit_pydantic as sp
from app.models.update_user import UpdateUser

def update_user_form() -> UpdateUser:
    with st.sidebar.container():
        data = sp.pydantic_form(key="update_user", model=UpdateUser, submit_label="Atualizar", clear_on_submit=True)

    return data
