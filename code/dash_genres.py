#!/usr/bin/env python
# coding: utf-8

# In[72]:


import pandas as pd
import plotly.express as px
import streamlit as st


# In[73]:


movies=pd.read_csv(r"C:\Users\Admin\Desktop\Project2\Data to work on\MOVIE_filtered.zip",compression="zip", low_memory=False)


# In[74]:


st.sidebar.header('Filters')

years = movies['startYear'].dropna().sort_values().unique().tolist()
year_min, year_max = int(min(years)), int(max(years))
selected_year = st.sidebar.slider('Select year range', year_min, year_max, (year_min, year_max))

genre_list = set([genre for sublist in movies['genres'].dropna().str.split(',') for genre in sublist])
selected_genres = st.sidebar.multiselect('Select genres', genre_list)


rating_min, rating_max = float(movies['averageRating'].min()), float(movies['averageRating'].max())
selected_rating = st.sidebar.slider('Select minimum rating', rating_min, rating_max, rating_min)

filtered_df = movies[
    (movies['startYear'] >= selected_year[0]) & 
    (movies['startYear'] <= selected_year[1]) &
    (movies['averageRating'] >= selected_rating)
]

if selected_genres:
    filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]


# In[75]:


filtered_df['genres'] = filtered_df['genres'].astype(str)
filtered_df['genres'] = filtered_df['genres'].str.split(',')
exploded_df = filtered_df.explode('genres')

exploded_df['Profit'] = exploded_df['revenue'] - exploded_df['budget']


# In[76]:


genres_selection = ["Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Drama",
    "Family",
    "Fantasy",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller"]

filtered_genres = exploded_df[exploded_df['genres'].isin(genres_selection)]


# In[80]:


genre_avg_profit = filtered_genres.groupby('genres')['Profit'].mean().reset_index()
genre_avg_profit = genre_avg_profit.sort_values(by='Profit', ascending=False)

fig1 = px.bar(genre_avg_profit, 
             x='genres', 
             y='Profit', 
             title='Average Profit by Genre',
             color='Profit')

fig1.update_layout(xaxis_tickangle=45,
    xaxis_title='Genre',
    yaxis_title='Average Profit'
)






# In[81]:


# Get rid of duplicates and find the best 1000 movies
unique_tconst = filtered_genres['tconst'].unique()[:1000]
# filter
filtered_df2 = filtered_genres[exploded_df['tconst'].isin(unique_tconst)]
#List of genres in 1000 best films
genre_counts = filtered_df2['genres'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']

fig2 = px.bar(genre_counts, 
             x='Genre', 
             y='Count', 
             title='Frequency of Each Genre in the TOP 1000 Films',
             color='Count')

fig2.update_layout(xaxis_tickangle=45,
    xaxis_title='Genre',
    yaxis_title='Count'
)




# In[88]:


# Create the new col with decade
def categorize_into_decade(year):
    return (year // 10) * 10

filtered_genres['Decade'] = filtered_genres['startYear'].apply(categorize_into_decade)
# df with frequency of each genre per decade
genre_counts_over_decades = filtered_genres.groupby(['Decade', 'genres']).size().reset_index(name='count')

fig3 = px.line(genre_counts_over_decades, x='Decade', y='count', color='genres',
              title='Number of Films per Genre Over Decades',
              labels={'count': 'Number of Films', 'Decade': 'Decade'},
              line_shape='spline')

fig3.update_layout(xaxis_tickangle=30,
    xaxis_title='Decade',
    yaxis_title='Number of Films',
    legend_title='Genre',
    legend=dict(orientation="v", y=1, x=0, xanchor='left', yanchor='top')
)





# In[89]:


# same with the percentage of number of films per each genre through the decades

genre_counts_over_decades = filtered_genres.groupby(['Decade', 'genres']).size().reset_index(name='Film Count')
total_films_per_decade = filtered_genres.groupby('Decade').size().reset_index(name='Total Films')

merged_data = pd.merge(genre_counts_over_decades, total_films_per_decade, on='Decade')
merged_data['Percentage'] = (merged_data['Film Count'] / merged_data['Total Films']) * 100

fig4 = px.line(merged_data, x='Decade', y='Percentage', color='genres',
              title='Percentage of Films per Genre Over Decades',
              labels={'Percentage': 'Percentage of Total Films', 'Decade': 'Decade'},
              line_shape='spline')

fig4.update_layout(
    xaxis_title='Decade',
    yaxis_title='Percentage of Total Films',
    legend_title='Genre',
    legend=dict(orientation="v", y=1, x=0, xanchor='left', yanchor='top')
)





# In[83]:


st.header('Movie Genres Data')

with st.expander("Select Graphs to Display"):
    show_graph_1 = st.checkbox('Average Profit by Genre', True)
    show_graph_2 = st.checkbox('Frequency of Each Genre in the TOP 1000 Films', True)
    show_graph_3 = st.checkbox('Number of Films per Genre Over Decades', True)
    show_graph_4 = st.checkbox('Percentage of Films per Genre Over Decades', True)

graphs_selected = sum([show_graph_1, show_graph_2, show_graph_3, show_graph_4])

def create_graph_column(fig, col):
    with col:
        st.plotly_chart(fig, use_container_width=True)

if graphs_selected == 1:
    if show_graph_1:
        st.plotly_chart(fig1, use_container_width=True)
    elif show_graph_2:
        st.plotly_chart(fig2, use_container_width=True)
    elif show_graph_3:
        st.plotly_chart(fig3, use_container_width=True)
    elif show_graph_4:
        st.plotly_chart(fig4, use_container_width=True)

elif graphs_selected == 2:
    cols = st.columns(2)
    graphs = [show_graph_1, show_graph_2, show_graph_3, show_graph_4]
    figures = [fig1, fig2, fig3, fig4]
    displayed = 0
    for i, graph in enumerate(graphs):
        if graph:
            create_graph_column(figures[i], cols[displayed % 2])
            displayed += 1

else:
    first_row = st.columns(2)
    second_row = st.columns(2)
    graphs = [show_graph_1, show_graph_2, show_graph_3, show_graph_4]
    figures = [fig1, fig2, fig3, fig4]
    displayed = 0
    for i, graph in enumerate(graphs):
        if graph:
            if displayed < 2:
                create_graph_column(figures[i], first_row[displayed % 2])
            else:
                create_graph_column(figures[i], second_row[displayed % 2])
            displayed += 1


# In[ ]:





# In[ ]:




