import streamlit as st

st.set_page_config(
    page_title="Bonjour LimouZen",
    page_icon="🎬",
    layout="wide")

with st.sidebar:
    with st.container():
        st.image("images/Logo-limouzen_wide.png")

st.markdown("""<style>
            body { max-width: 1200px; margin: auto;}
            .names h3{
                color: #006699;
                margin-top:-15px;
                margin-bottom:-15px;
            }
            .names {
                text-align: center;
            }
            </style>""", unsafe_allow_html=True)


with st.container():
    st.markdown("<h1 style='text-align: center; color:#006699; margin-top:-80px;'>BONJOUR<br>LimouZen Cinéma</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#006699;margin-bottom:-40px;'>Notre équipe :</h2>", unsafe_allow_html=True)
    st.header("", divider='rainbow')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://static.streamlit.io/examples/cat.jpg")
        st.markdown("<div class='names'><h3>Marton</h3><p>DataViz et Machine learning</p></div>", unsafe_allow_html=True)
    with col2:
        st.image("https://static.streamlit.io/examples/cat.jpg")
        st.markdown("<div class='names'><h3>Thomas</h3><p>Recherche secteur et Dataviz</p></div>", unsafe_allow_html=True)
    with col3:
        st.image("https://static.streamlit.io/examples/cat.jpg")
        st.markdown("<div class='names'><h3>Maximilien</h3><p>Data-base et Scrum-Master</p></div>", unsafe_allow_html=True)