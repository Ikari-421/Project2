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

with st.container(border=True):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Le marché du cinéma", "Module de recherche", "Analyse KPIs 1",
                            "Analyse KPIs 2", "Secteur géographique"
                            ])
    with tab1:
        st.markdown("<h3 class='title-tab'>Recommandations marché :</h3>", unsafe_allow_html=True)
        st.markdown("""<div class='flex-container'>
                        <div class="items-images">
                            <img src='' alt='Image''>
                        </div>
                        <div class="items-text">
                            <ul>
                                <li><b>Rotation</b> plus importante des films en <b>période de pointe</b>.
                                </li>
                                <li><b>Privilégier les genres préférés des Français</b>.
                                </li>
                            <ul/>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    with tab2:
        st.markdown("<h3 class='title-tab'>Recommandations module de recherche :</h3>", unsafe_allow_html=True)
        st.markdown("""<div class='flex-container'>
                        <div class="items-images">
                            <img src='' alt='Image''>
                        </div>
                        <div class="items-text">
                            <ul>
                                <li>Notre système de recommandation est performant et fonctionnel, de <b>nombreuses fonctionnalités sont possibles</b>.
                                </li>
                                <li><b>Suivi des activités</b> de recherche, <b>réalisation d'un tableau de bord</b> d'activité...
                                </li>
                                <li>Toutefois, <b>nous ne sommes pas développeurs d'applications web</b>.
                                </li>
                                <li>La <b>mise en contact</b> avec des <b>professionnels</b> du secteur est <b>indispensable</b>.
                                </li>
                            <ul/>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    with tab3:
        st.markdown("<h3 class='title-tab'>Recommandations analyse KPIs 1:</h3>", unsafe_allow_html=True)
        st.markdown("""<div class='flex-container'>
                        <div class="items-images">
                            <img src='' alt='Image''>
                        </div>
                        <div class="items-text">
                            <ul>
                                <li><b>Prioriser</b> les films des <b>réalisateurs du top 10 de popularité</b>.
                                </li>
                                <li>Comme <b>Christopher Nolan, Steven Spielberg, Quentin Tarantino, Martin Scorsese</b>...
                                </li>
                                <li>Voir graphique : <b>Classement des réalisateurs en fonction de la popularité</b>.
                                </li>
                            <ul/>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    with tab4:
        st.markdown("<h3 class='title-tab'>Recommandations analyse KPIs 2:</h3>", unsafe_allow_html=True)
        st.markdown("""<div class='flex-container'>
                        <div class="items-images">
                            <img src='' alt='Image''>
                        </div>
                        <div class="items-text">
                            <ul>
                                <li><b>Prioriser</b> les films des <b>genres les plus rentables tels que</b>.
                                </li>
                                <li>Les films d'<b>animation</b>, d'<b>aventure</b> et de <b>science-fiction</b>, des compagnies telles que <b>Marvel Studios</b>, <b>Lucasfilm</b>...
                                </li>
                                <li>Voir graphique : <b>Top 10 des compagnies de production par moyenne de profit par film</b>.
                                </li>
                            <ul/>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    with tab5:
        st.markdown("<h3 class='title-tab'>Recommandations secteur géographique :</h3>", unsafe_allow_html=True)
        st.markdown("""<div class='flex-container'>
                        <div class="items-images">
                            <img src='' alt='Image''>
                        </div>
                        <div class="items-text">
                            <ul>
                                <li><b>Créer un concept</b> particulier de cinéma pour attirer <b>la population</b> en dehors de la zone de chalandise.
                                </li>
                                <li><b>Concept cinéma vintage</b>, pour jouer sur <b>la nostalgie</b> d'une population vieillissante.
                                </li>
                                <li>Le concept : programmation <b>hebdomadaire</b> jours thématiques générationnels. <i>voir annexe</i>.
                                </li>
                            <ul/>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
