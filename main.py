import streamlit as st
import pandas as pd

from DataProvider import DataProvider


@st.cache_data
def data_init():
    with st.spinner("Wait for data..."):
        data_provider = DataProvider()

        return data_provider


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


def init_week_inputs(week_inputs):
    input_cols = st.columns(3)

    for i in range(st.session_state.weeks):
        with input_cols[i % 3]:
            week_inputs.append(
                st.number_input(
                    f"Listening time in week {i + 1}",
                    min_value=0,
                    value=5,
                    key=f"input-{i}",
                )
            )
    return week_inputs


def init_artist_visualization(artist_data, data_provider):
    selected_artists = st.multiselect("Select artists", data_provider.get_artists())

    for artist in selected_artists:
        try:
            artist_data[artist] = data_provider.get_x_and_y([artist])[0][0, :, 0]
        except KeyError:
            st.error(f"Artist {artist} not found")
    if len(artist_data) > 0:
        st.line_chart(pd.DataFrame(artist_data))


def main():
    week_inputs = []
    artist_data = {}
    if "weeks" not in st.session_state:
        st.session_state.weeks = 6

    data_provider = data_init()

    init_header()
    init_buttons()
    init_week_inputs(week_inputs)

    st.divider()
    st.header("Predicted listening time")
    listening_data = {
        "Listening time": week_inputs,
        "Listening time - 5": [x - 5 for x in week_inputs],
    }
    st.line_chart(pd.DataFrame(listening_data))

    st.divider()
    init_artist_visualization(artist_data, data_provider)


if __name__ == "__main__":
    main()
