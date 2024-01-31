#!/usr/bin/env python
# coding: utf-8

# In[173]:


import pandas as pd
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# In[174]:

file = "C:\Users\Admin\Desktop\Project2\Data to work on"
background_color = "#1f2833"
text_color = "white"           


# In[175]:


movies=pd.read_csv("./MOVIE_filtered.zip" ,compression="zip", low_memory=False)


# In[184]:


st.sidebar.header('Filters')

years = movies['startYear'].dropna().sort_values().unique().tolist()
year_min, year_max = int(min(years)), int(max(years))
selected_year = st.sidebar.slider('Select year range', year_min, year_max, (year_min, year_max))

genre_list = set([genre for sublist in movies['genres'].dropna().str.split(',') for genre in sublist])
selected_genres = st.sidebar.multiselect('Select genres', genre_list)

language_list = movies['original_language'].dropna().unique().tolist()
selected_languages = st.sidebar.multiselect('Select languages', language_list)

rating_min, rating_max = float(movies['averageRating'].min()), float(movies['averageRating'].max())
selected_rating = st.sidebar.slider('Select minimum rating', rating_min, rating_max, rating_min)

filtered_df = movies[
    (movies['startYear'] >= selected_year[0]) & 
    (movies['startYear'] <= selected_year[1]) &
    (movies['averageRating'] >= selected_rating)
]

if selected_genres:
    filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]

if selected_languages:
    filtered_df = filtered_df[movies['original_language'].isin(selected_languages)]




# In[178]:


filtered_df['production_companies_name'] = movies['production_companies_name'].apply(
    lambda x: x if isinstance(x, list) else x.replace('[', '').replace(']', '').replace("'", '').split(','))


# In[179]:


exploded_df = filtered_df.explode('production_companies_name')


# In[180]:


cleaned_movies = exploded_df[exploded_df['production_companies_name'] != '']


# In[181]:


cleaned_movies.loc[:, 'production_companies_name'] = cleaned_movies['production_companies_name'].str.lstrip()


# In[182]:


top_5000=cleaned_movies.head(5000)


# In[183]:


company_movie_counts = cleaned_movies.groupby('production_companies_name')['tconst'].nunique()

top_10_companies = company_movie_counts.sort_values(ascending=False).head(10)
top_10_companies_df = top_10_companies.reset_index()
top_10_companies_df.columns = ['Production Company', 'Number of Movies']


# In[164]:


import plotly.express as px
fig1 = px.bar(top_10_companies_df, 
             x='Production Company', 
             y='Number of Movies',
             color_discrete_sequence=["darkgoldenrod"])
fig1.update_layout(
    title={
        'text': 'Top 10 Production Companies by Number of Movies',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            color='white')
    },
    xaxis_title=None,
    yaxis_title=None,
    xaxis_tickangle=30,
    plot_bgcolor=background_color,
    paper_bgcolor=background_color,
    font=dict(color="white"))

fig1.update_xaxes(title_font=dict(color='white'), tickfont=dict(color='white'))
fig1.update_yaxes(title_font=dict(color='white'), tickfont=dict(color='white'))





# In[154]:


top_1000 = cleaned_movies.head(1000)
company_movie_counts2 = top_1000.groupby('production_companies_name')['tconst'].nunique()
top_10_companies2 = company_movie_counts2.sort_values(ascending=False).head(10)
top_10_companies_df2 = top_10_companies.reset_index()
top_10_companies_df2.columns = ['Production Company', 'Number of Movies']






# In[165]:


fig2 = px.bar(top_10_companies2, 
    title='Top 10 Production Companies in Top 1000 Highest Ranked Films',
    labels={'value': 'Number of Films', 'index': 'Production Company'},
    color_discrete_sequence=['darkgoldenrod']
)                 

fig2.update_layout(
    title={
        'text': 'Top 10 Production Companies in Top 1000 Highest Ranked Films',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(color='white')},
    plot_bgcolor=background_color,
    paper_bgcolor=background_color,
    font=dict(color="white"),
    xaxis_title=None,
    yaxis_title=None
)
fig2.update_xaxes(title_font=dict(color='white'), tickfont=dict(color='white'))
fig2.update_yaxes(title_font=dict(color='white'), tickfont=dict(color='white'))
fig2.update_layout(showlegend=False)


# In[167]:


top_5000['Profit'] = top_5000['revenue'] - top_5000['budget']
total_profit_by_company = top_5000.groupby('production_companies_name')['Profit'].sum()

most_successful_companies = total_profit_by_company.sort_values(ascending=False).head(10)
most_successful_companies_df = most_successful_companies.reset_index()
most_successful_companies_df.columns = ['Production Company', 'Total Profit']


fig3 = px.bar(most_successful_companies_df, 
             y='Production Company', 
             x='Total Profit',
             color_discrete_sequence=['darkgoldenrod'], 
             orientation='h',)

fig3.update_layout(
    title={
        'text': 'Top 10 Most Successful Production Companies by Profit',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(color='white')},
    plot_bgcolor=background_color,
    paper_bgcolor=background_color,
    font=dict(color="white"),
    xaxis_title=None,
    yaxis_title=None
)



fig3.update_xaxes(title_font=dict(color='white'), tickfont=dict(color='white'))
fig3.update_yaxes(title_font=dict(color='white'), tickfont=dict(color='white'))



# In[168]:


top_5000['Profit'] = top_5000['revenue'] - top_5000['budget']
film_count_by_company = top_5000['production_companies_name'].value_counts()

companies_at_least_10_films = film_count_by_company[film_count_by_company >= 10].index
filtered_df = top_5000[top_5000['production_companies_name'].isin(companies_at_least_10_films)]

avg_profit_by_company = filtered_df.groupby('production_companies_name')['Profit'].mean()
top_companies_by_avg_profit = avg_profit_by_company.sort_values(ascending=False).head(10)
top_companies_by_avg_profit_df = top_companies_by_avg_profit.reset_index()
top_companies_by_avg_profit_df.columns = ['Production Company', 'Average Profit']

fig4 = px.bar(top_companies_by_avg_profit_df, 
             x='Average Profit', 
             y='Production Company', 
             title='Top 10 Production Companies by Average Profit per Film (Min 10 Films)',
             orientation='h',
             color_discrete_sequence=['darkgoldenrod'])
fig4.update_layout(
     title={
        'text': 'Top 10 Production Companies by Average Profit per Film (Min 10 Films)',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(color='white')},
     plot_bgcolor=background_color,
     paper_bgcolor=background_color,
     font=dict(color="white"),
     xaxis_title=None,
     yaxis_title=None)

fig4.update_xaxes(title_font=dict(color='white'), tickfont=dict(color='white'))
fig4.update_yaxes(title_font=dict(color='white'), tickfont=dict(color='white'))


# In[203]:


companies_per_year = cleaned_movies.groupby('startYear')['production_companies_name'].nunique().reset_index()

fig5 = px.line(
    companies_per_year, 
    x='startYear', 
    y='production_companies_name', 
    labels={'startYear': 'Year', 'production_companies_name': 'Number of Production Companies'},
    title='Number of Production Companies Over the Years',
    color_discrete_sequence=['darkgoldenrod'])

fig5.update_layout(
     title={
        'text': 'Number of Production Companies Over the Years',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(color='white')},
     plot_bgcolor=background_color,
     paper_bgcolor=background_color,
     font=dict(color="white"),
     xaxis_title=None,
     yaxis_title=None)



# In[205]:


import streamlit as st

st.header('Production Company Data')

with st.expander("Select Graphs to Display"):
    show_graph_1 = st.checkbox('Top 10 Production Companies by Number of Movies', True)
    show_graph_2 = st.checkbox('Top 10 Production Companies in Top 1000 Highest Ranked Films', True)
    show_graph_3 = st.checkbox('Top 10 Most Successful Production Companies by Profit', True)
    show_graph_4 = st.checkbox('Top 10 Production Companies by Average Profit per Film (Min 10 Films)', True)
    show_graph_5 = st.checkbox('Number of Production Companies Over the Years', True)

graphs_selected = sum([show_graph_1, show_graph_2, show_graph_3, show_graph_4, show_graph_5])

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
    elif show_graph_5:
        st.plotly_chart(fig5, use_container_width=True)

elif graphs_selected == 2:
    cols = st.columns(2)
    graphs = [show_graph_1, show_graph_2, show_graph_3, show_graph_4, show_graph_5]
    figures = [fig1, fig2, fig3, fig4, fig5]
    displayed = 0
    for i, graph in enumerate(graphs):
        if graph:
            create_graph_column(figures[i], cols[displayed % 2])
            displayed += 1

else:
    first_row = st.columns(2)
    second_row = st.columns(2)
    third_row = None
    graphs = [show_graph_1, show_graph_2, show_graph_3, show_graph_4, show_graph_5]
    figures = [fig1, fig2, fig3, fig4, fig5]
    displayed = 0
    for i, graph in enumerate(graphs):
        if graph:
            if displayed < 2:
                create_graph_column(figures[i], first_row[displayed % 2])
            elif displayed < 4:
                create_graph_column(figures[i], second_row[displayed % 2])
            else:
                if not third_row:
                    third_row = st.columns(2)
                create_graph_column(figures[i], third_row[displayed % 2])
            displayed += 1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




