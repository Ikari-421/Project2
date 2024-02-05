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

# User interface for selecting a movie title, genres, and actors
movie_options = np.insert(df_movies['originalTitle'].unique(), 0, 'None')
selected_movie = st.selectbox("Select a movie (optional):", options=movie_options)
selected_genres = st.multiselect("Select genres (optional):", options=np.sort(df_movies['genres'].str.split(',', expand=True).stack().unique()))
selected_actors = st.multiselect("Select actor(s) (optional):", options=np.sort(df_movies['actors_actresses'].str.split(',', expand=True).stack().unique()))
num_recommendations = st.slider("Select the number of recommendations:", 1, 10, 6)

# function to split strings into list of str
def splitter(value):
    """Split comma-separated strings into a list."""
    return value.split(',') if isinstance(value, str) else []

# function for one hot encoding cols
def create_dummy_columns(df, names_list, column_name, df_column):
    """Create dummy columns for categorical variables"""
    for name in names_list:
        if name:
            name = name.strip()
            df[column_name + name] = df[df_column].apply(lambda x: 1 if isinstance(x, str) and name in x else 0)

# The main function to make recommendations
def get_recommendations(movie_title, selected_genres, selected_actors, num_recs):
    top30000 = df_movies
    
    # Filter by selected genres
    if selected_genres:
        top30000 = top30000[top30000['genres'].apply(lambda x: any(genre.strip() in [g.strip() for g in str(x).split(',')] for genre in selected_genres) if x else False)]

    # Filter by selected actors
    if selected_actors:
        top30000 = top30000[top30000['actors_actresses'].apply(lambda x: any(actor.strip() in [a.strip() for a in str(x).split(',')] for actor in selected_actors) if x else False)]

    # Re-include the selected movie if it's been filtered out
    if movie_title != 'None' and movie_title not in top30000['originalTitle'].values:
        selected_movie_df = df_movies[df_movies['originalTitle'] == movie_title]
        top30000 = pd.concat([top30000, selected_movie_df], ignore_index=True)
    
    # Running knn if a title is selected.
    if movie_title != 'None':
        # Getting the index of the seleted film then create dummies of categoricals
        index_movie = top30000.loc[top30000["originalTitle"] == movie_title].index[0]
        actors_in_chosen_film = splitter(top30000.iloc[index_movie]['actors_actresses'])
        directors_in_chosen_film = splitter(top30000.iloc[index_movie]['directors'])
        writers_in_chosen_film = splitter(top30000.iloc[index_movie]['writers'])
        genres = splitter(top30000.iloc[index_movie]['genres'])

        create_dummy_columns(top30000, actors_in_chosen_film, 'actor_', 'actors_actresses')
        create_dummy_columns(top30000, directors_in_chosen_film, 'director_', 'directors')
        create_dummy_columns(top30000, writers_in_chosen_film, 'writer_', 'writers')
        create_dummy_columns(top30000, genres, 'genre_', 'genres')
        
        #making knn df with only numerical cols
        df_knn = top30000.drop(columns=['tconst', 'genres', 'overview', 'poster_path', 'originalTitle', 'actors_actresses', 'directors', 'writers', 'averageRating', 'numVotes'])
        X = df_knn
        # scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        # fit model with user specified number of negbours
        model = NearestNeighbors(n_neighbors=num_recs)
        model.fit(X_scaled)
        # finding the recommendations in the original dataset and filtering cols to show
        recommendation_indices = model.kneighbors([X_scaled[index_movie], ])[1][0]
        recommended_movies = top30000.iloc[recommendation_indices][['originalTitle', 'runtimeMinutes', 'genres', 'startYear', 'averageRating', 'numVotes', 'actors_actresses', 'directors', 'overview', 'poster_path']]
    else:
        # If no movie title selected the system recommends the best rated movies with the users chosen genres or actors
        recommended_movies = top30000.head(num_recs)

    recommended_movies = recommended_movies.set_index('originalTitle')
    return recommended_movies

if st.button("Get Recommendations"):
    recommendations = get_recommendations(selected_movie, num_recommendations + 1)
    recommendations_head = recommendations.head(1)
    recommendations = recommendations.iloc[1:,:]

    cols = [None, None, None] 


    for index, (title, row) in enumerate(recommendations_head.iterrows()):

        with st.container():
            col1, col2 = st.columns([5, 7])

            with col1:
                image_path = 'https://image.tmdb.org/t/p/original/'+row['poster_path']
                html_image = f"<img src='{image_path}' alt='Image' style='width: 100%; border-radius:14px;box-shadow: 1px 1px 15px 1px #c4c4c4;'>"
                st.markdown(html_image, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

            st.markdown("""<style>
                        .head_movie {
                            padding: 20px; 
                        }
                        .head_movie h2 {
                            color: #606060;
                        }
                        .head_movie li, .head_movie p span {
                            font-size:14px;
                            color: #606060;
                        }
                        .head_movie li span{
                            font-size:18px;
                            font-weight: bold;
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
                            margin-bottom:-15px;
                        }
                        .blur-container p{
                            font-size:14px;
                            margin-top:-45px
                            height:90%;
                        }
                        .blur-container h2{
                            text-shadow: 0px 0px 8px #fff;
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
                runtimeMinutes = str(int(row['runtimeMinutes']))
                startYear = str(row['startYear'])
                directors = str(row['directors'])
                actors_actresses = str(row['actors_actresses'])
                averageRating = str(round(row['averageRating'],2))
                overview = row['overview']

                st.markdown(f"""
                            <div class='head_movie'>
                                <h2>{title}</h2>
                                <ul style='list-style-type:none;'>
                                    <li>Durée: <span>{runtimeMinutes} minutes</span></li>
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
        if index % 4 == 0:
            cols = st.columns(4) 

        with cols[index % 4]:
            with st.container(border=True):
                image_path = 'https://image.tmdb.org/t/p/original/'+row['poster_path']
                html_image = f"<img src='{image_path}' alt='Image' style='width: 100%; border-radius:8px;box-shadow: 1px 1px 15px 1px #c4c4c4;'>"
                st.markdown(html_image, unsafe_allow_html=True)

                runtimeMinutes = str(int(row['runtimeMinutes']))
                startYear = str(row['startYear'])
                directors = str(row['directors'])
                actors_actresses = str(row['actors_actresses'])
                averageRating = str(round(row['averageRating'],2))
                overview = row['overview']

                st.markdown(f"""<div class='blur-container'>
                            <h2>{title}</h2>
                            <p>
                                Durée: <span>{runtimeMinutes}</span> minutes</br>
                                Année: <span>{startYear}</span></br>
                                Réalisateur(trice): <span>{directors}</span></br>
                                <!-- Acteurs(trices): <span>{actors_actresses}</span></br> -->
                                Note IMBD: <span>{averageRating}</span></br>
                            </p>
                            </div>""",
                            unsafe_allow_html=True)

                st.markdown(f"""<div style='height:5px;'>
                            </div>""",
                            unsafe_allow_html=True)