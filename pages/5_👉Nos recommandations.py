import streamlit as st

st.set_page_config(
    page_title="Nos recommanddations",
    page_icon="👉",
    layout="wide")

with st.sidebar:
    st.image("images/Logo-squarecharts_wide_2.png")

# User interface for selecting a movie title, genres, and actors
with st.container():
    image_path = "https://github.com/Ikari-421/Project2/blob/master/images/Logo-limouzen_square.png?raw=true"
    html_image = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top: -50px;">
        <img src='{image_path}' alt='Image' style="height:200px;">
    </div>"""
    st.markdown(html_image, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color:#52527a;'>Nos recommandations</h1>", unsafe_allow_html=True)
    st.header("", divider='grey')