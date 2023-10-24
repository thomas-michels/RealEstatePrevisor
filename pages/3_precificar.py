import streamlit as st
import streamlit_pydantic as sp
from app.models import SellingProperty
from app.services import predict_property_price


st.write("# Precifique seu imóvel")
st.write("Para precificar seu imovel será necessário algumas informações dele.")

with st.expander("Imovel"):
    data = sp.pydantic_form(key="Imovel", model=SellingProperty, submit_label="Precificar", clear_on_submit=True)

if data:
    with st.spinner("Precificando..."):
        try:
            predicted_price = predict_property_price(property=data)

            st.write("## Confira os preços previstos abaixo")
            st.balloons()
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Preço minimo", value=f"R$ {(predicted_price.predicted_price - predicted_price.mse):,}")
            col2.metric(label="Preço previsto", value=f"R$ {predicted_price.predicted_price:,}")
            col3.metric(label="Preço máximo", value=f"R$ {(predicted_price.predicted_price + predicted_price.mse):,}")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(label="Quartos", value=predicted_price.property.rooms)
            col2.metric(label="Banheiros", value=predicted_price.property.bathrooms)
            col3.metric(label="Garagens", value=predicted_price.property.parking_space)
            col4.metric(label="Tamanho em m²", value=predicted_price.property.size)

        except Exception as error:
            st.error(error.args[0], icon="🚨")
