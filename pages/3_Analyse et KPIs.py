import streamlit as st
import head_master as hm
import pandas as pd


st.set_page_config(
    page_title="Analyse et KPIs",
    page_icon="📈",
    layout="wide")

# import matplotlib
# import plotly
# import sklearn
# st.title('plotly=='+plotly.__version__)
# st.title('matplotlib=='+matplotlib.__version__)

url = "./src_data/"
csv_movies = pd.read_csv(url+"MOVIE_filtered.zip" ,compression="zip", low_memory=False)
# st.dataframe(csv_movies)
title_principals = pd.read_csv(url+"principlals_filtered.zip" ,compression="zip", low_memory=False)

name_basics = pd.read_csv(url+"names_filtered.zip" ,compression="zip", low_memory=False)


st.markdown("""<style>
            .names h3{
                color: #006699;
                margin-top:-15px;
                margin-bottom:-15px;
            }
            .names {
                text-align: center;
            }
            .title-tab {
                color:#3e82a4;
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
                color:FireBrick;
            }
            .inner-text li{
                font-size:18px;
                margin-bottom:15px;
            }
            .inner-text b{
                color:orange;
            }
            </style>""", unsafe_allow_html=True)

#-----------------
#    SIDE BAR
#-----------------

with st.sidebar:
    with st.container():
        st.header('Filters')

        # Système de filtre
        years = csv_movies['startYear'].dropna().sort_values().unique().tolist()
        year_min, year_max = int(min(years)), int(max(years))
        selected_year = st.sidebar.slider('Select year range', year_min, year_max, (year_min, year_max))

        genre_list = set([genre for sublist in csv_movies['genres'].dropna().str.split(',') for genre in sublist])
        selected_genres = st.sidebar.multiselect('Select genres', genre_list)

        rating_min, rating_max = float(csv_movies['averageRating'].min()), float(csv_movies['averageRating'].max())
        selected_rating = st.sidebar.slider('Select minimum rating', rating_min, rating_max, rating_min)

        filtered_df = csv_movies[
            (csv_movies['startYear'] >= selected_year[0]) & 
            (csv_movies['startYear'] <= selected_year[1]) &
            (csv_movies['averageRating'] >= selected_rating)
        ]

        if selected_genres:
            filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]

    st.image("images/Logo-limouzen_wide.png")

#-----------------
#    MAIN
#-----------------

with st.container():
    st.markdown("<h1 style='text-align: center; color:##2c2e58; margin-top:-80px;'>📈 Analyse et KPIs</h1>", unsafe_allow_html=True)
    # st.markdown("<h2 style='color:#006699;margin-bottom:-40px;'>Les Graphiques:</h2>", unsafe_allow_html=True)
    st.header("", divider='rainbow')

with st.container(border=True):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Analyse secteur", "Finances", "Production companies",
                                            "Acteurs / directeur / écrivant","Genre"
                                            ])
    with tab1:
        st.markdown("""<h3 class='title-tab'>Analyse secteur</h3>
                    """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3 class='title-tab'>Finances</h3>", unsafe_allow_html=True)
        hm.charts_core("finance_charts", filtered_df)

    with tab3:
        st.markdown("<h3 class='title-tab'>Production companies</h3>", unsafe_allow_html=True)
        hm.production_charts(filtered_df)

    with tab4:
        st.markdown("<h3 class='title-tab'>Acteurs / directeur / écrivant</h3>", unsafe_allow_html=True)
        hm.actors_charts(csv_movies, title_principals, name_basics)

    with tab5:
        st.markdown("<h3 class='title-tab'>Genres</h3>", unsafe_allow_html=True)
        hm.genres_charts(filtered_df)