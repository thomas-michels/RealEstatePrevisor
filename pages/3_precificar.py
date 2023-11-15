from typing import List, Tuple
import streamlit as st
import streamlit_pydantic as sp
from app.models import SellingProperty
from app.services import predict_property_price, PropertySearch

st.write("# Precifique seu imóvel")
st.write("Para precificar seu imovel será necessário algumas informações dele.")


def get_data(
        page_size: int=10,
        offset: int=0,
        rooms: int=0,
        bathrooms: int=0,
        parking_space: int=0,
        size: int=0,
        zip_code: str=""):

    property_search = PropertySearch()

    data = property_search.find_similar_properties(
        page_size=page_size,
        offset=offset,
        rooms=rooms,
        bathrooms=bathrooms,
        parking_space=parking_space,
        size=size,
        zip_code=zip_code
    )
    return data

def calculate_prices(properties: List[dict], predicted_price) -> Tuple[float, float]:
    min_price = predicted_price
    max_price = predicted_price

    if isinstance(properties, list):
        for property in properties:
            if property["price"] <= min_price:
                min_price = property["price"]

            if property["price"] >= max_price:
                max_price = property["price"]

    return min_price, max_price

with st.expander("Imovel"):
    model_id = st.number_input(label="ID do Modelo", min_value=0)
    data = sp.pydantic_form(key="Imovel", model=SellingProperty, submit_label="Precificar", clear_on_submit=False)

if data:
    with st.spinner("Precificando..."):
        try:
            predicted_price = predict_property_price(model_id=model_id, property=data)

            if isinstance(predicted_price, str):
                st.warning(predicted_price, icon="🚨")

            else:
                st.write("## Confira os preços previstos abaixo")
                st.balloons()

                properties = get_data(
                    rooms=data.quartos,
                    bathrooms=data.banheiros,
                    parking_space=data.garagens,
                    size=data.tamanho,
                    zip_code=data.cep
                )

                min_price, max_price = calculate_prices(properties, predicted_price.predicted_price)
                price_confidence = round(((predicted_price.predicted_price - predicted_price.mse) / predicted_price.predicted_price) * 100, 2)
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Preço minimo", value=f"R$ {(min_price):,}")
                col2.metric(label="Preço previsto", value=f"R$ {predicted_price.predicted_price:,}", delta=f"{price_confidence}%")
                col3.metric(label="Preço máximo", value=f"R$ {(max_price):,}")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(label="Quartos", value=predicted_price.property.rooms)
                col2.metric(label="Banheiros", value=predicted_price.property.bathrooms)
                col3.metric(label="Garagens", value=predicted_price.property.parking_space)
                col4.metric(label="Tamanho em m²", value=predicted_price.property.size)

            st.divider()

            if properties:
                if not isinstance(properties, str):
                    st.write("### Alguns imóveis similares")
                    for property in properties:
                        col1, col2, col3 = st.columns(3)
                        col2.image(property["image_url"], width=300)

                        col1, col2, col3 = st.columns(3)
                        col1.metric(label="Preço", value=f"R$ {(property['price']):,}")

                        col1, col2, col3, col4 = st.columns(4)

                        col1.metric(label="Quartos", value=property["rooms"])
                        col2.metric(label="Banheiros", value=property["bathrooms"])
                        col3.metric(label="Garagens", value=property["parking_space"])
                        col4.metric(label="Tamanho em m²", value=property["size"])
                        st.write(f"Mais detalhes no [link]({property['property_url']}).")
                        st.divider()

        except Exception as error:
            st.error(error.args[0], icon="🚨")
