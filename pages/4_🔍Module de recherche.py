import streamlit as st
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer

url = "./src_data/"
df_movies = pd.read_csv(url+"new_features.csv")

st.set_page_config(
    page_title="Module de recherche",
    page_icon="📽️",
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
    st.markdown("<h1 style='text-align: center; color:#52527a;'>Module de recherche</h1>", unsafe_allow_html=True)
    st.header("", divider='grey')

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        movie_options = np.insert(df_movies['originalTitle'].unique(), 0, '')
        selected_movie = st.selectbox("Select a movie (optional):", options=movie_options)
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_genres = st.multiselect("Select genres (optional):", options=np.sort(df_movies['genres'].str.split(',', expand=True).stack().unique()))
    with col2:
        selected_actors = st.multiselect("Select actor(s) (optional):", options=np.sort(df_movies['actors_actresses'].str.split(',', expand=True).stack().unique()))
    with col3:
        num_recommendations = st.slider("Select the number of recommendations:", 1, 10, 8)

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


def title_to_words(title, stop_words):
    """Convert movie titles into a list of words, excluding stopwords."""
    if not isinstance(title, str):
        return []
    
    words = title.lower().split()  # Convert to lowercase and split by space
    filtered_words = [word for word in words if word not in stop_words]
    return filtered_words

def create_dummy_words(df, names_list, column_name_prefix, stop_words,col):
    """Create dummy columns for words in movie titles, excluding stopwords."""
    for name in names_list:
        column_name = f"{column_name_prefix}{name}"
        if column_name not in df.columns:
            df[column_name] = df[col].apply(
                lambda x: 1 if name in title_to_words(x, stop_words) else 0
            )

# Function to calculate similarity and sort movies
def sort_recommendations_by_overview_similarity(selected_movie_overview, recommendations_df):
    # Assuming the 'overview' column exists in recommendations_df
    if selected_movie_overview:
        overviews = recommendations_df['overview'].fillna('').tolist()
        overviews.insert(0, selected_movie_overview)  # Insert at the beginning for comparison

        # Vectorize the overviews using TF-IDF
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(overviews)

        # Calculate cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

        # Assign similarity scores back to the DataFrame
        recommendations_df['similarity_score'] = cosine_sim.flatten()
        #recommendations_df['similarity_score'] = recommendations_df['similarity_score'].apply(np.sqrt)
        #recommendations_df['similarity_score'] = recommendations_df['similarity_score']/2

        # Sort based on similarity score
        sorted_recommendations = recommendations_df.sort_values(by='similarity_score', ascending=False)
        return sorted_recommendations
    else:
        # If no overview available for the selected movie, return the DataFrame as is
        return recommendations_df

def get_actor_based_recommendations(selected_actors, num_recs, exclude_title=None):
    """Generate recommendations based on actors, excluding a specific title if given."""
    actor_movies = df_movies[df_movies['actors_actresses'].apply(lambda x: any(actor in x for actor in selected_actors) if isinstance(x, str) else False)]
    if exclude_title:
        actor_movies = actor_movies[actor_movies['originalTitle'] != exclude_title]
    actor_movies = actor_movies.sort_values(by='averageRating', ascending=False).head(num_recs)
    return actor_movies
def combine_recommendations(primary_recommendations, actor_based_recommendations, num_recs):
    # Remove potential duplicates when combining by dropping duplicates based on a unique identifier (e.g., movie ID or title)
    combined = pd.concat([primary_recommendations, actor_based_recommendations]).drop_duplicates(subset='originalTitle')
    
    # Sort combined recommendations by actor_match and any other criteria
    combined_sorted = combined.sort_values(by=['actor_match', 'similarity_score'], ascending=[False, False])
    
    return combined_sorted.head(num_recs)
# The main function to make recommendations
def get_recommendations(movie_title, selected_genres, selected_actors, num_recs):
    top30000 = df_movies.copy()
    
    if selected_actors:
        top30000 = top30000[top30000['actors_actresses'].apply(lambda x: isinstance(x, str) and any(actor in x for actor in selected_actors))]
    
    # Apply genre filtering if any genres are selected
    if selected_genres:
        top30000 = top30000[top30000['genres'].apply(lambda x: any(genre.strip() in str(x).split(',') for genre in selected_genres) if x else False)]
    #set n_neighbors to avoid error, def 65
    n_neighbors = min(len(top30000),60)

    if n_neighbors > 0:

        # Include the selected movie for comparison if it's not None and not already in the filtered dataset
        if movie_title != 'None' and movie_title not in top30000['originalTitle'].values:
            selected_movie_df = df_movies[df_movies['originalTitle'] == movie_title]
            top30000 = pd.concat([top30000, selected_movie_df], ignore_index=True)


        # Running knn if a title is selected.
        if movie_title != 'None':
            # Getting the index of the seleted film then create dummies of categoricals
            # Retrieve the overview of the selected movie       
            selected_movie_overview = df_movies[df_movies['originalTitle'] == movie_title]['overview'].iloc[0]       

            stop_words = set(['the', 'and', 'of', 'in', 'a', 'to', 'is', 'it', 'with', 'as', 'for', 'on', 'at', 'by', 'an'])

            index_movie = top30000.loc[top30000["originalTitle"] == movie_title].index[0]
            actors_in_chosen_film = splitter(top30000.iloc[index_movie]['actors_actresses'])
            directors_in_chosen_film = splitter(top30000.iloc[index_movie]['directors'])
            writers_in_chosen_film = splitter(top30000.iloc[index_movie]['writers'])
            genres = splitter(top30000.iloc[index_movie]['genres'])
            title_words= title_to_words(top30000.iloc[index_movie]['originalTitle'],stop_words)
            prod_company= splitter(top30000.iloc[index_movie]['production_companies_name'])

            create_dummy_columns(top30000, actors_in_chosen_film, 'actor_', 'actors_actresses')
            create_dummy_columns(top30000, directors_in_chosen_film, 'director_', 'directors')
            create_dummy_columns(top30000, writers_in_chosen_film, 'writer_', 'writers')
            create_dummy_columns(top30000, genres, 'genre_', 'genres')
            create_dummy_words(top30000, title_words, 'word_', stop_words,'originalTitle')
            create_dummy_columns(top30000, prod_company, 'production', 'production_companies_name')

        
            #making knn df with only numerical cols
            df_knn = top30000.drop(columns=['tconst','genres', 'overview', 'production_companies_name','poster_path', 'originalTitle', 'actors_actresses', 'directors', 'writers', 'averageRating', 'numVotes'])
            df_knn = df_knn.apply(pd.to_numeric, errors='ignore')

            X = df_knn
            # scaling
            scaler = StandardScaler()
            #scaler = RobustScaler()
            X_scaled = scaler.fit_transform(X)
            # fit model with user specified number of negbours
            model = NearestNeighbors(n_neighbors=n_neighbors)
            model.fit(X_scaled)
            # finding the recommendations in the original dataset and filtering cols to show
            recommendation_indices = model.kneighbors([X_scaled[index_movie], ])[1][0]
            recommended_movies = top30000.iloc[recommendation_indices][['originalTitle', 'runtimeMinutes', 'genres', 'startYear', 'averageRating', 'numVotes', 'actors_actresses', 'directors', 'overview', 'poster_path']]
            recommended_movies = sort_recommendations_by_overview_similarity(selected_movie_overview, recommended_movies)
            recommended_movies= recommended_movies.set_index('originalTitle')

        
    else:
        # Inform the user that no films match their specified criteria
        st.warning("We couldn't find any films matching your criteria. Try adjusting your selections for broader results.Here are some movies that you might like based on your genre selection")
        
        top30000 = df_movies.copy()
        top30000 = top30000[top30000['genres'].apply(lambda x: any(genre.strip() in str(x).split(',') for genre in selected_genres) if x else False)]
        #set n_neighbors to avoid error, def 65
        n_neighbors = min(len(top30000), 22)
        
        # Include the selected movie for comparison if it's not None and not already in the filtered dataset
        if movie_title != 'None' and movie_title not in top30000['originalTitle'].values:
                selected_movie_df = df_movies[df_movies['originalTitle'] == movie_title]
                top30000 = pd.concat([top30000, selected_movie_df], ignore_index=True)
      
        
    
        # Running knn if a title is selected.
        if movie_title != 'None':
            # Getting the index of the seleted film then create dummies of categoricals
            # Retrieve the overview of the selected movie       
            selected_movie_overview = df_movies[df_movies['originalTitle'] == movie_title]['overview'].iloc[0]       
       
            stop_words = set(['the', 'and', 'of', 'in', 'a', 'to', 'is', 'it', 'with', 'as', 'for', 'on', 'at', 'by', 'an'])

            index_movie = top30000.loc[top30000["originalTitle"] == movie_title].index[0]
            actors_in_chosen_film = splitter(top30000.iloc[index_movie]['actors_actresses'])
            directors_in_chosen_film = splitter(top30000.iloc[index_movie]['directors'])
            writers_in_chosen_film = splitter(top30000.iloc[index_movie]['writers'])
            genres = splitter(top30000.iloc[index_movie]['genres'])
            title_words= title_to_words(top30000.iloc[index_movie]['originalTitle'],stop_words)
            prod_company= splitter(top30000.iloc[index_movie]['production_companies_name'])

            create_dummy_columns(top30000, actors_in_chosen_film, 'actor_', 'actors_actresses')
            create_dummy_columns(top30000, directors_in_chosen_film, 'director_', 'directors')
            create_dummy_columns(top30000, writers_in_chosen_film, 'writer_', 'writers')
            create_dummy_columns(top30000, genres, 'genre_', 'genres')
            #create_dummy_words(top30000, title_words, 'word_', stop_words,'originalTitle')
            create_dummy_columns(top30000, prod_company, 'production', 'production_companies_name')

        
            #making knn df with only numerical cols
            df_knn = top30000.drop(columns=['tconst','genres', 'overview', 'production_companies_name','poster_path', 'originalTitle', 'actors_actresses', 'directors', 'writers', 'averageRating', 'numVotes'])
            df_knn = df_knn.apply(pd.to_numeric, errors='ignore')

            X = df_knn
            # scaling
            scaler = StandardScaler()
            #scaler = RobustScaler()
            X_scaled = scaler.fit_transform(X)
            # fit model with user specified number of negbours
            model = NearestNeighbors(n_neighbors=n_neighbors)
            model.fit(X_scaled)
            # finding the recommendations in the original dataset and filtering cols to show
            recommendation_indices = model.kneighbors([X_scaled[index_movie], ])[1][0]
            recommended_movies = top30000.iloc[recommendation_indices][['originalTitle', 'runtimeMinutes', 'genres', 'startYear', 'averageRating', 'numVotes', 'actors_actresses', 'directors', 'overview', 'poster_path']]
            recommended_movies = sort_recommendations_by_overview_similarity(selected_movie_overview, recommended_movies)
            recommended_movies= recommended_movies.set_index('originalTitle')
    return recommended_movies

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
                border-radius:8px;
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
            .center {
                display: flex;
                justify-content: center;
            }
            </style>""", unsafe_allow_html=True)

####The STREAMLIT layout and buttons configuration
btn_statment = st.button("Get Recommendations")

if btn_statment:
    # Fetch recommendations, potentially with one extra to exclude the selected movie later
    adjusted_num_recs = num_recommendations  if selected_movie != 'None' else num_recommendations
    recommendations = get_recommendations(selected_movie, selected_genres, selected_actors, adjusted_num_recs)

    if isinstance(recommendations, str):
            # If recommendations is a string, display it as a message(when no movie found)
            st.write(recommendations)

    if selected_movie != '':
        movie_details = df_movies[df_movies['originalTitle'] == selected_movie].iloc[0]


        with st.container():
            # Create a two-column layout
            col1, col2 = st.columns([5, 7])  # Adjust the ratio as needed

            # Column 1: Displaying the selected movie's image
            with col1:
                image_path = 'https://image.tmdb.org/t/p/original/'+movie_details['poster_path']
                html_image = f"<img src='{image_path}' alt='Image' style='width: 100%; border-radius:14px;box-shadow: 1px 1px 15px 1px #c4c4c4;'>"
                st.markdown(html_image, unsafe_allow_html=True)

            # Separator
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

            # Column 2: Displaying the selected movie's details next to the image
            with col2:
                title = str(movie_details['originalTitle'])
                runtimeMinutes = str(int(movie_details['runtimeMinutes']))
                startYear = str(movie_details.get('startYear', 'N/A'))
                directors = str(movie_details.get('directors', 'N/A'))
                actors_actresses = str(movie_details.get('actors_actresses', 'N/A'))
                averageRating = str(round(movie_details['averageRating'],2))
                overview = movie_details['overview']

                # st.write(f"**Year:** {movie_details.get('startYear', 'N/A')}")
                # st.write(f"**Director(s):** {movie_details.get('directors', 'N/A')}")
                # st.write(f"**Actor(s):** {movie_details.get('actors_actresses', 'N/A')}")
                # st.write("**Description:**")
                # st.write(movie_details.get('overview', 'No description available.'))

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

            # Exclude the selected movie from recommendations if it's in the list
            recommendations = recommendations[recommendations.index != selected_movie]

    # only the requested number of recommendations
    recommendations = recommendations.head(adjusted_num_recs)

    st.subheader('Nos recomandation')
    # Show recommendations
    cols = [None, None, None]
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