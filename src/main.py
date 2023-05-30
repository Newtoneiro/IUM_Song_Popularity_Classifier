import streamlit as st
import pandas as pd

from DataProvider import DataProvider
from main_models import LinearRegressionModel, LSTMModel


@st.cache_data
def data_init():
    with st.spinner("Loading data..."):
        data_provider = DataProvider()

        return data_provider


@st.cache_resource
def load_model():
    with st.spinner("Loading model..."):
        naive_model = LinearRegressionModel()
        lstm_model = LSTMModel()
        return naive_model, lstm_model


# These are callback functions for buttons
def add_week():
    st.session_state.weeks += 1


def remove_week():
    st.session_state.weeks -= 1


def init_header():
    st.title("IUM Project")
    st.header("Music Listening Time Predictor For Pozytywka Company")
    st.write("---")


def init_buttons():
    button_cols = st.columns(2)

    with button_cols[0]:
        st.button("Add week", on_click=add_week, use_container_width=True)
    with button_cols[1]:
        st.button("Remove week", on_click=remove_week, use_container_width=True)


def init_week_inputs(week_inputs, init_data):
    input_cols = st.columns(3)
    for i, val in enumerate(init_data):
        with input_cols[i % 3]:
            week_inputs.append(
                st.number_input(
                    f"Listening time in week {i + 1}",
                    min_value=0.0,
                    value=val,
                    key=f"input-{i}",
                )
            )
    return week_inputs


def predict(model, week_inputs, future_points):
    with st.spinner("Predicting..."):
        return model.predict([x for x in week_inputs], future_points)


def main():
    week_inputs = []
    artist_data = [0.0]

    naive_model, lstm_model = load_model()

    if "weeks" not in st.session_state:
        st.session_state.weeks = 6

    data_provider = data_init()

    init_header()

    isCustomData = st.checkbox("Custom data")
    if not isCustomData:
        selected_artist = st.selectbox(
            "Preload artist data", data_provider.get_consistent_artists()
        )
        artist_data = data_provider.get_x_and_y([selected_artist])[0].squeeze()
    else:
        init_buttons()
        artist_data = [0.0 for _ in range(st.session_state.weeks)]

    st.divider()

    init_week_inputs(week_inputs, artist_data)

    future_points = st.slider("Future points", min_value=1, max_value=10, value=5)

    st.divider()
    st.header("Predicted listening time")

    listening_data = {
        "Naive prediction": predict(naive_model, week_inputs, future_points),
        "LSTM prediction": predict(lstm_model, week_inputs, future_points),
        "Listening time": [x for x in week_inputs]
        + [None for _ in range(future_points)],
    }
    st.line_chart(pd.DataFrame(listening_data))

    st.divider()


if __name__ == "__main__":
    main()
