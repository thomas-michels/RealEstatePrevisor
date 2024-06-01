import streamlit as st
from st_pages import Page, show_pages, hide_pages
from app.components.login_sidebar import get_login_form
from app.components.logged_state import get_logged
from app.services.user import UserService


def get_side_bar(current_path: str):

    user_service = UserService(token="")

    with st.sidebar:
        st.title("Get Imóveis")

        if st.session_state.get("current_user"):
            user_service.set_token(new_token=st.session_state.get("token"))
            current_user = st.session_state.get("current_user")
            get_logged(current_user)

            show_pages(
                [
                    Page("1_home.py", "Home", "🏠"),
                    Page("pages/6_listagem_de_imoveis.py", "Busca de Imóveis", "🔍"),
                    Page("pages/2_mapa_de_imoveis.py", "Mapa de Imóveis", "🗺️"),
                ]
            )

            hide_pages(
                [
                    Page("pages/3_precificar.py", "Precificação", "🪧"),
                    Page("pages/4_treinar_modelo.py", "Treinamento de Modelos de IA", "🪧"),
                    Page("pages/5_exibir_resultados.py", "Resultados", "🪧"),
                ]
            )

        else:
            if current_path != "home":
                st.switch_page("1_home.py")

            else:

                data = get_login_form()

                show_pages(
                    [
                        Page("1_home.py", "Home", "🏠"),
                    ]
                )

                hide_pages(
                    [
                        Page("pages/6_listagem_de_imoveis.py", "Busca de Imóveis", "🔍"),
                        Page("pages/2_mapa_de_imoveis.py", "Mapa de Imóveis", "🗺️"),
                        Page("pages/3_precificar.py", "Precificação", "🪧"),
                        Page("pages/4_treinar_modelo.py", "Treinamento de Modelos de IA", "🪧"),
                        Page("pages/5_exibir_resultados.py", "Resultados", "🪧"),
                    ]
                )

                if data:
                    success, token = user_service.login(data=data)

                    if success:
                        user_service.set_token(new_token=token)
                        success, current_user = user_service.me()

                        if success:
                            st.session_state["token"] = token
                            st.session_state["current_user"] = current_user
                            st.rerun()

                    else:
                        st.toast(body=token, icon="🚨")
