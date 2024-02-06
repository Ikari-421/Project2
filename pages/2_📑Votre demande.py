import streamlit as st

st.set_page_config(
    page_title="Votre demande",
    page_icon="📑",
    layout="wide")

with st.sidebar:
    with st.container():
        st.image("images/Logo-squarecharts_wide_2.png")

st.markdown("""<style>
            .names h3{
                color: #52527a;
                margin-top:-15px;
                margin-bottom:-15px;
            }
            .names {
                text-align: center;
            }
            .title-tab {
                color:#52527a;
                margin-bottom:10px;
            }
            .inner-text ul{
                margin-top:25px;
                margin-left:45px;
            }
            .inner-text p{
                margin-top:35px;
                margin-left:-55px;
                padding-right:20px;
                color:#333366;
            }
            .inner-text li{
                font-size:18px;
                margin-bottom:15px;
            }
            .inner-text b{
                color:orange;
            }
            </style>""", unsafe_allow_html=True)

with st.container():
    image_path = "https://github.com/Ikari-421/Project2/blob/master/images/Logo-limouzen_square.png?raw=true"
    html_image = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top: -50px;">
        <img src='{image_path}' alt='Image' style="height:200px;">
    </div>"""
    st.markdown(html_image, unsafe_allow_html=True)
    # st.header("", divider='grey')
    st.markdown("<h2 style='color:#52527a;margin-top:30px;'>Nos missions:</h2>", unsafe_allow_html=True)
    # st.header("", divider='grey')

with st.container(border=True):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Notre travail", "Nos démarches", "Les outils",
                            "Les difficultés", "Améliorations"
                            ])
    with tab1:
        st.markdown("<h3 class='title-tab'>Présentation de notre travail</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/Team_work.gif", use_column_width="auto")
        with col2:
            st.markdown(f"""<div class='inner-text'>
                        <ul>
                            <li>Étude du marché de <b>La Creuse</b>
                            </li>
                            <li>Prise d'info sur l'activité du <b>cinéma</b>
                            </li>
                            <li>Obtenir quelques <b>statistiques</b> sur les films
                            </li>
                            <li>Système de <b>recommandation</b> de <b>films</b>
                            </li>
                            <li><b>Conclusion</b> et <b>pistes d’amélioration.</b>
                            </li>
                        <ul/>
                        <p><i>
                        Après étude, nous avons conclu qu'il était nécessaire de filtrer les bases de données, car le nombre de films Indiens représente une trop grande proportion des résultats.
                        </i></p>
                        </div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3 class='title-tab'>Nos démarches effectuées</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/Team_goals.gif", use_column_width="auto")
        with col2:
            st.markdown(f"""<div class='inner-text'>
                        <ul>
                            <li>Recherche internet pour l'étude Métier<br>
                                <i>Source : Insee</i> 
                            </li>
                            <li>Mise en place de la méthode <b>Agil-Scrum</b>
                            </li>
                            <li>Filtrage et réorganisation des bases de données
                            </li>
                            <li>Extraction des <b>KPIs</b>
                            </li>
                            <li>Création d'un model de recommandation
                            </li>
                            <li>Nos recommandation métier
                            </li>
                        <ul/>
                        </div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("<h3 class='title-tab'>Les outils utilisés</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:st.markdown(f"""<div class='inner-text'>
                        <ul>
                            <li>La méthode <b>Agil-Scrum</b>
                            </li>
                            <li>Langage <b>Python</b> pour la programmation
                            </li>
                            <li><b>Pandas</b> et <b>Numpy</b> pour la structure des données
                            </li>
                            <li><b>Matplotlib</b> et <b>Seaborn</b> la visualisation des graphiques
                            </li>
                            <li><b>SciKit Learn</b> pour model de Machine Learning
                            </li>
                            <li><b>Streamlit</b> pour cette incroyable présentation
                            </li>
                        <ul/>
                        </div>""", unsafe_allow_html=True)
        with col2:
            st.image("images/Maintenance.gif", use_column_width="auto")
            
    with tab4:
        st.markdown("<h3 class='title-tab'>Difficultés rencontrées</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:st.markdown(f"""<div class='inner-text'>
                        <ul>
                            <li>Base de données très lourde importer besoin de nettoyage important
                            </li>
                            <li>Après analyse de la base complète IMDB <b>Sur-représentation</b> des films <b>Indiens</b>
                            </li>
                            <li>Difficulté de <b>compréhention</b> de la demande du <b>projet</b>
                            </li>
                            <li>Affinage du model de <b>Machine Learning</b> assez long
                            </li>
                            <li>Mise en place de <b>Streamlit</b>
                            </li>
                        <ul/>
                        </div>""", unsafe_allow_html=True)
        with col2:
            st.image("images/Dizzy_face.gif", use_column_width="auto")
# 3e82a4
    with tab5:
        st.markdown("<h3 class='title-tab'>Nos pistes d'améliorations</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/Good_team.gif", use_column_width="auto")
        with col2:st.markdown(f"""<div class='inner-text'>
                        <ul>
                            <li style="margin-top:55px;">Utilisation de modèle <b>N L P</b> (Natural Language Processing)
                            </li>
                            <li><b>historique</b> de recherche de <b>films</b> du client
                            </li>
                            <li><b>Explication du projet</b> plus claire et précise
                            </li>
                            <li>Accès aux données des <b>client</b> et <b>cinéma</b>
                            </li>
                        <ul/>
                        </div>""", unsafe_allow_html=True)
