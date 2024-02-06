import streamlit as st

st.set_page_config(
    page_title="Bonjour LimouZen",
    page_icon="🎬",
    layout="wide")

with st.sidebar:
    with st.container():
        st.image("images/Logo-squarecharts_wide.png")

st.markdown("""<style>
            body { max-width: 1200px; margin: auto; color:#333366; }
            .our_logo{
                margin:50px 0 50px 0;
                display:flex;
                justify-content:center;
            }
            .our_logo div{
                display:flex;
                align-items:center;
            }
            .our_logo img{
                width:150px; 
                border-radius:14px;
            }
            .our_logo p{
                padding: 0px 40px 0px 40px;
                width:600px;
            }
            .names h3{
                color: #333366;
                margin-top:-15px;
                margin-bottom:-15px;
            }
            .names {
                text-align: center;
            }
            .profil_container{
                width:auto;
                display:flex;
                justify-content:space-evenly;
            }
            .profil{
                display:flex;
                background: #fff;
                padding:25px;
                border-radius:8px;
                border: silver solid 0px;
                box-shadow: 0px 0px 6px 1px #c4c4c4;
                flex-direction:column;
                align-items:center;
                width:25%;
                margin-top:35px;
            }
            .profil img{
                width:150px;
                border:#333366 solid 4px;
                border-radius:50%;
                box-shadow: 1px 1px 15px 1px #c4c4c4;
            }
            .profil h3{
                color: #996699;
                margin-top:30px;
            }
            .profil p, .profil h3{
                text-shadow: 0px 0px 8px #fff;
            }
            </style>""", unsafe_allow_html=True)

with st.container():
    # st.markdown("<h1 style='text-align: center; color:#006699; margin-top:0px;'>BONJOUR</h1>", unsafe_allow_html=True)
    image_path = "https://github.com/Ikari-421/Project2/blob/master/images/Logo-limouzen_square.png?raw=true"
    html_image = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top: -50px;">
        <img src='{image_path}' alt='Image' style="height:200px;">
    </div>"""
    st.markdown(html_image, unsafe_allow_html=True)

    st.markdown("<h2 style='color:#006699;margin-bottom:-40px;'>Notre équipe :</h2>", unsafe_allow_html=True)
    st.header("", divider='rainbow')

    image_path = "https://github.com/Ikari-421/Project2/blob/master/images/logo-squarecharts.png?raw=true"
    html_image = f"""
    <div class="our_logo">
        <div>
        <img src='{image_path}' alt='Image'>
            <p>
            <b> Square Charts</b>, spécialiste de l'analyse de données, présente une analyse approfondie du marché du cinéma, accompagnée d'un modèle de recommandation de films personnalisé.
            </p>
        </div>
    </div>"""
    st.markdown(html_image, unsafe_allow_html=True)



    image_marton = "https://github.com/Ikari-421/Project2/blob/master/images/marton.png?raw=true"
    image_thomas = "https://github.com/Ikari-421/Project2/blob/master/images/thomas.png?raw=true"
    image_max = "https://github.com/Ikari-421/Project2/blob/master/images/maximilien.png?raw=true"

    st.markdown(f"""
                <div class="profil_container">
                    <div class="profil">
                        <img src='{image_marton}' alt='Image'>
                        <div class='names'><h3>Marton</h3>
                            <p>DataViz et Machine learning</p>
                        </div>
                    </div>
                    <div class="profil">
                        <img src='{image_thomas}' alt='Image'>
                        <div class='names'><h3>Thomas</h3>
                            <p>Recherche secteur et Dataviz</p>
                        </div>
                    </div>
                    <div class="profil">
                        <img src='{image_max}' alt='Image'>
                        <div class='names'><h3>Maximilien</h3>
                            <p>Data-base,  et Scrum-Master</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # import pandas as pd
    # import seaborn as sns
    # import sys
    # st.write("Panda version", pd. __version__)
    # st.write("seaborn version", sns. __version__)
    # st.write("streamlit version", st. __version__)
    # st.write("Python version", sys.version)