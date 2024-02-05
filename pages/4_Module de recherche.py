import streamlit as st
# from head_master import *
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

url = "./src_data/"
df_movies = pd.read_csv(url+"ml_data.csv")

st.set_page_config(
    page_title="Analyse et KPIs",
    page_icon="📈",
    layout="wide")

st.title("Movie Recommendation System")
selected_movie = st.selectbox("Select a movie for recommendations:", df_movies['originalTitle'].unique())
num_recommendations = st.slider("Select the number of recommendations:", 1, 10, 6)

def get_recommendations(movie_title,num_recs):
    top30000 = df_movies.head(5000).reset_index(drop=True)

    index_movie = top30000.loc[top30000["originalTitle"] == selected_movie].index[0]
    def splitter(value):
        return value.split(',') if isinstance(value, str) else []

    actors_in_chosen_film = splitter(top30000.iloc[index_movie]['actors_actresses'])
    directors_in_chosen_film = splitter(top30000.iloc[index_movie]['directors'])
    writers_in_chosen_film = splitter(top30000.iloc[index_movie]['writers'])
    genres = splitter(top30000.iloc[index_movie]['genres'])

    def create_dummy_columns(df, names_list, column_name, df_column):
        for name in names_list:
            if name:
                name = name.strip()
                df[column_name + name] = df[df_column].apply(
                    lambda x: 1 if isinstance(x, str) and name in x else 0)

    create_dummy_columns(top30000, actors_in_chosen_film, 'actor_', 'actors_actresses')
    create_dummy_columns(top30000, directors_in_chosen_film, 'director_', 'directors')
    create_dummy_columns(top30000, writers_in_chosen_film, 'writer_', 'writers')
    create_dummy_columns(top30000, genres, 'genre_', 'genres')


    df_knn = top30000.drop(columns=['tconst', 'genres','overview','poster_path', 'originalTitle', 'actors_actresses', 'directors', 'writers','averageRating','numVotes'])
    X = df_knn

    weight=1
    for col in df_knn.columns:
        if col.startswith('genre_'):
            df_knn[col] *= weight

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = NearestNeighbors(n_neighbors=10)
    model.fit(X_scaled)

    recommendation = model.kneighbors([X_scaled[index_movie], ])[1][0]
    recommended_movies = top30000.iloc[recommendation][['originalTitle', 'runtimeMinutes', 'genres', 'startYear', 'averageRating', 'numVotes', 'actors_actresses', 'directors', 'overview', 'poster_path']]
    recommended_movies = recommended_movies.set_index('originalTitle')

    return recommended_movies.head(num_recs)

if st.button("Get Recommendations"):
    recommendations = get_recommendations(selected_movie, num_recommendations + 1)
    recommendations_head = recommendations.head(1)
    recommendations = recommendations.iloc[1:,:]

    col_index = 0
    cols = [None, None, None] 


    for index, (title, row) in enumerate(recommendations_head.iterrows()):

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                
                image_path = 'https://image.tmdb.org/t/p/original/'+row['poster_path']
                
                html_image = f"<img src='{image_path}' alt='Image' style='width: 100%; border-radius:14px;box-shadow: 1px 1px 15px 1px #c4c4c4;'>"
                
                st.markdown(html_image, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

            st.markdown("""<style>
                        .head_movie h2 {
                            color: #606060; 
                        }
                        .head_movie li, .head_movie p span {
                            font-size:14px; 
                            font-weight: bold;
                            color: #606060;
                        }
                        .head_movie li span{
                            font-size:18px; 
                            font-weight: normal;
                            color: #000000;
                        }
                        .head_movie p{
                            font-size:18px;
                        }        
                        .blur-container {
                            background-color: rgba(255, 255, 255, 0.4);
                            height:95%;
                            padding-left: 20px;
                            padding-right: 20px;
                            padding-top: -20px;
                            backdrop-filter: blur(10px);
                            margin-top:-80px;
                            width:100.25%;
                            margin-bottom:-15px
                            border: red solid 1px;
                        }
                        .blur-container p{
                            font-size:14px;
                            margin-top:-45px
                            height:90%;
                        }
                        .blur-container h2{
                            text-shadow: 0px 0px 5px #fff;
                            text-align:center;
                            font-weight: bolder;
                            font-size:20px;
                            height:80px;
                        }
                        .blur-container p span{
                            font-weight: 300;
                            font-size:18px;
                        }
                        </style>""", unsafe_allow_html=True)

            with col2:
                runtimeMinutes = str(row['runtimeMinutes'])
                startYear = str(row['startYear'])
                directors = str(row['directors'])
                actors_actresses = str(row['actors_actresses'])
                averageRating = str(round(row['averageRating'],2))
                overview = row['overview']

                st.markdown(f"""<div style='padding: 20px;' class='head_movie'>
                            <h2>{title}</h2>
                            <ul style='list-style-type:none;'>
                                <li>Durée: <span>{runtimeMinutes}</span></li>
                                <li>Année: <span>{startYear}</span></li>
                                <li>Réalisateur(trice): <span>{directors}</span></li>
                                <li>Acteurs(trices): <span>{actors_actresses}</span></li>
                                <li>Note IMBD: <span>{averageRating}</span></li>
                            </ul>
                            <p><span>Description:</span><br>
                            {overview}
                            </p>
                            </div>""",
                            unsafe_allow_html=True)

    st.subheader('Nos recomandation')

    for index, (title, row) in enumerate(recommendations.iterrows()):
        if index % 3 == 0:
            cols = st.columns(3) 

        with cols[index % 3]:
            with st.container(border=True):
                image_path = 'https://image.tmdb.org/t/p/original/'+row['poster_path']
                html_image = f"<img src='{image_path}' alt='Image' style='width: 100%; border-radius:8px;box-shadow: 1px 1px 15px 1px #c4c4c4;'>"
                st.markdown(html_image, unsafe_allow_html=True)

                runtimeMinutes = str(row['runtimeMinutes'])
                startYear = str(row['startYear'])
                directors = str(row['directors'])
                actors_actresses = str(row['actors_actresses'])
                averageRating = str(round(row['averageRating'],2))
                overview = row['overview']

                st.markdown(f"""<div class='blur-container'>
                            <h2>{title}</h2>
                            <p>
                                Durée: <span>{runtimeMinutes}</span></br>
                                Année: <span>{startYear}</span></br>
                                Réalisateur(trice): <span>{directors}</span></br>
                                Acteurs(trices): <span>{actors_actresses}</span></br>
                                Note IMBD: <span>{averageRating}</span></br>
                            </p>
                            </div>""",
                            unsafe_allow_html=True)

                st.markdown(f"""<div style='height:5px;'>
                            </div>""",
                            unsafe_allow_html=True)