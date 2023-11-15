import streamlit as st
import streamlit_pydantic as sp
from streamlit_elements import mui, elements
from app.services import ModelService
from app.models import GWOParams, SummarizedModel, ModelStatus
import datetime

st.set_page_config(layout="wide")

def train_model(name: str, gwo_params: GWOParams) -> SummarizedModel:
    model_services = ModelService()
    
    if "train_lock" not in st.session_state:
        summarized_model = model_services.train_new_model(name=name, gwo_params=gwo_params)

        if summarized_model:
            st.session_state["train_lock"] = summarized_model.id
            st.session_state["summarized_model"] = summarized_model

            return summarized_model

def search_model(model_id: int) -> SummarizedModel:
    model_services = ModelService()

    summarized_model = model_services.get_model_by_id(model_id=model_id)

    if summarized_model.status == ModelStatus.READY and st.session_state.get("train_lock") == summarized_model.id:
        st.session_state.pop("train_lock")
    
    if summarized_model:
        st.session_state["summarized_model"] = summarized_model

    return summarized_model

st.write("# Treinar novo modelo")
with st.expander(label="Parametro para treino"):
    try:
        name = st.text_input(label="Nome do modelo")
        gwo_params = sp.pydantic_form(key="Parametros", model=GWOParams, submit_label="Treinar", clear_on_submit=False)

        in_training = train_model(name=name, gwo_params=gwo_params)

        if st.session_state.get("summarized_model") and not st.session_state.get("popup"):
            st.session_state["popup"] = True
            st.toast(body=f"Seu modelo está sendo treinado - #{st.session_state['summarized_model'].id}", icon="😎")

    except Exception as error:
        print(f"Error on train model -> {str(error)}")

col1, col2, col3 = st.columns(3)
refresh = col2.button("Atualizar progresso")

if st.session_state.get("summarized_model") and refresh:
    
    try:
        in_training = st.session_state.get("summarized_model")

        if in_training:

            if (datetime.datetime.now(in_training.created_at.tzinfo) - in_training.created_at) < datetime.timedelta(seconds=10):
                st.toast(f"Aguarde mais alguns segundos para atualizar!", icon="🚨")

            else:
                st.divider()
                in_training = search_model(model_id=in_training.id)

                now = datetime.datetime.now(tz=datetime.timezone.utc)

                diff = (now - in_training.created_at).total_seconds()

                if in_training.remaining_time_in_seconds > 0:
                    value = (diff / in_training.remaining_time_in_seconds) * 100
                    progress = min(1.0, max(0.0, value / 100))

                else:
                    progress = 1.0

                st.write(f"## Modelo #{in_training.id} - {in_training.name}")

                st.progress(value=progress, text="Acompanhe o progresso do treinamento")

                if in_training.remaining_time_in_seconds == 0:
                    st.balloons()
                    st.toast("Seu modelo foi treinado com sucesso", icon="🚀")

                col1, col2, col3 = st.columns(3)

                col2.write(f"Tempo estimado em segundos - {in_training.remaining_time_in_seconds}s")

    except Exception as error:
        print(f"Error on update progress -> {str(error)}")

st.divider()

st.write("# Modelos treinados")

def get_data(page: int, page_size: int, refresh: bool=False):
    model_service = ModelService()

    if "models" not in st.session_state or refresh:
        st.session_state["models"] = model_service.get_models(page=page, page_size=page_size)

    return st.session_state["models"]

with elements("table"):
    data = get_data(page=1, page_size=10, refresh=refresh)
    with mui.TableHead(width="100%"):
        mui.TableCell("ID", x=0, y=0, w=2, h=2, moved=False)
        mui.TableCell("Nome", x=8, y=0, w=2, h=2, moved=False)
        mui.TableCell("MSE", x=12, y=0, w=2, h=2, moved=False)
        mui.TableCell("Grey Wolf Parametros", x=16, y=0, w=4, h=2, moved=False)
        mui.TableCell("Treinado em", x=20, y=0, w=2, h=2, moved=False)

    with mui.TableBody(width="100%"):
        for i, model in enumerate(data, 1):
            with mui.TableRow():
                mui.TableCell(model.id, x=0, y=i*4, w=2, h=2, moved=False)
                mui.TableCell(model.name, x=2, y=i*4, w=4, h=2, moved=False)
                mui.TableCell(model.mse, x=4, y=i*4, w=2, h=2, moved=False)
                mui.TableCell(str(model.gwo_params), x=6, y=i*4, w=4, h=2, moved=False)
                mui.TableCell(model.updated_at.strftime("%d/%m/%Y"), x=8, y=i*4, w=2, h=2, moved=False)