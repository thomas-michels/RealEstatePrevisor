import streamlit as st
from streamlit_elements import mui, elements
from app.services import ModelService
from app.models import ModelWithHistory
from typing import List
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.write("# Exibindo resultados de um modelo")

def get_data(page: int, page_size: int, refresh: bool=False):
    model_service = ModelService()

    if "models" not in st.session_state or refresh:
        st.session_state["models"] = model_service.get_models(page=page, page_size=page_size)

    data = {}

    for model in st.session_state["models"]:
        data[model.id] = model

    return data

def get_x_y_from_data(selected_model: ModelWithHistory, x: str = "epoch", y: str = "mse"):
    if x.__contains__("params."):
        new_x = x.replace("params.", "")

    else:
        new_x = x

    if y.__contains__("params."):
        new_y = y.replace("params.", "")

    else:
        new_y = y

    formatted_data = {
        new_x: [],
        new_y: []
    }

    for history in selected_model.history:
        if x.__contains__("params."):
            if new_x == "hidden_layer_sizes":
                formatted_data[new_x].append(history.params[new_x][0])

            else:
                formatted_data[new_x].append(history.params[new_x])

        else:
            formatted_data[new_x].append(getattr(history, x))

        if y.__contains__("params."):
            if new_x == "hidden_layer_sizes":
                formatted_data[new_y].append(history.params[new_y][0])
            
            else:
                formatted_data[new_y].append(history.params[new_y])

        else:
            formatted_data[new_y].append(getattr(history, y))

    return formatted_data, new_x, new_y

def get_history_params(selected_model: ModelWithHistory):
    main_keys = list(selected_model.history[0].dict().keys())
    main_keys.remove("model_id")
    main_keys.remove("created_at")
    main_keys.remove("updated_at")
    main_keys.remove("params")
    param_keys = list(selected_model.history[0].params.keys())
    new_param = []
    
    for key in param_keys:
        new_param.append(f"params.{key}")

    return (main_keys + new_param)

with st.spinner("Carregando..."):
    data = get_data(page=1, page_size=10)

col1, col2, col3 = st.columns(3)
option = col1.selectbox("Escolha um modelo treinado", (f"#{model.id} - {model.name}" for model in data.values()))

st.divider()

index = option.index(" -")
model_id = "".join(list(option)[1:index])

selected_model = data[int(model_id)]
st.write(f"## Modelo Selecionado - {selected_model.name}")

col1, col2 = st.columns(2)
col1.metric(label="MSE", value=selected_model.mse)

coordinates, x, y = get_x_y_from_data(selected_model)
st.line_chart(data=coordinates, x=x, y=y, use_container_width=True, width=1000, height=400)

params = get_history_params(selected_model)

st.divider()

col1, col2, col3 = st.columns(3)
option = col1.multiselect("Escolha 2 colunas para gerar o grafico: ", params, max_selections=2)

if len(option) == 2:
    coordinates, x, y = get_x_y_from_data(selected_model, option[0], option[1])
    st.line_chart(data=coordinates, x=x, y=y, use_container_width=True, width=1000, height=400)
