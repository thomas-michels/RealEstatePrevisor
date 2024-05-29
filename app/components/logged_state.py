import streamlit as st
from app.components.update_user import update_user_form
from app.models.user import User

def reset_current_user():
    if st.session_state.get("current_user"):
        st.session_state.pop("current_user")

    if st.session_state.get("token"):
        st.session_state.pop("token")


def get_logged(current_user: User):
    with st.sidebar.container():
        st.write(f"Bem vindo de volta {current_user.first_name}!")

        col1, col2 = st.columns(2)

        update_infos = col1.button(label="Atualizar informações")        
        col2.button(label="Sair", on_click=reset_current_user)
        
        if update_infos:
            updated = update_user_form()
            if updated:
                reset_current_user()
