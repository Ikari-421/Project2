#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import streamlit as st


# In[30]:


movies=pd.read_csv(r"C:\Users\Admin\Desktop\Project2\Data to work on\MOVIE_filtered.zip",compression="zip", low_memory=False)


# In[31]:


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
make_subplots

# In[32]:


filtered_df['Profit'] = filtered_df['revenue'] - filtered_df['budget']


# In[38]:


top_10_profitable_movies = filtered_df.sort_values(by='revenue', ascending=False).head(10)

fig1 = px.bar(top_10_profitable_movies, x='originalTitle', y='Profit',
             title='Top 10 Films by Profit',
             labels={'originalTitle': 'Film Title', 'Profit': 'Profit'},
             color='Profit')

fig1.update_layout(xaxis_tickangle=30,
    xaxis_title='Film Title',
    yaxis_title='Profit')



# In[34]:


top_10_by_revenue = filtered_df.sort_values(by='revenue', ascending=False).head(10)

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Bar(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['revenue'], name='Revenue'),
    secondary_y=False,)

fig2.add_trace(
    go.Bar(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['budget'], name='Budget'),
    secondary_y=False,)

fig2.add_trace(
    go.Scatter(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['Profit'], name='Profit', mode='lines+markers'),
    secondary_y=True,)

fig2.update_layout(xaxis_tickangle=30,
    title_text='Top 10 Films by Revenue, Budget, and Profit',
    barmode='group',)

fig2.update_xaxes(title_text='Film Title')
fig2.update_yaxes(title_text='Revenue / Budget', secondary_y=False)
fig2.update_yaxes(title_text='Profit', secondary_y=True)




# In[35]:


top_10_by_budget = filtered_df.sort_values(by='budget', ascending=False).iloc[1:11]


fig3 = px.bar(top_10_by_budget, x='originalTitle', y=['budget', 'Profit'],
                    title='Top 10 Films by Budget and Their Profits',
                    labels={'originalTitle': 'Film Title', 'value': 'Amount', 'variable': 'Type'})

fig3.update_layout(xaxis_tickangle=30,
    xaxis_title='Film Title',
    yaxis_title='Amount')




# In[36]:


top_10_by_revenue = filtered_df.sort_values(by='revenue', ascending=False).head(10)

fig4 = px.bar(top_10_by_revenue, x='originalTitle', y=['revenue', 'Profit'],
                     title='Top 10 Films by Revenue and Their Profits',
                     labels={'originalTitle': 'Film Title', 'value': 'Amount', 'variable': 'Type'})

fig4.update_layout(xaxis_tickangle=30,
    xaxis_title='Film Title',
    yaxis_title='Amount')



# In[39]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots


top_10_by_revenue = filtered_df.sort_values(by='revenue', ascending=False).head(10)


fig5 = make_subplots(specs=[[{"secondary_y": True}]])
fig5.add_trace(
    go.Bar(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['revenue'], name='Revenue'),
    secondary_y=False)


fig5.add_trace(
    go.Scatter(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['Profit'], name='Profit', mode='lines+markers'),
    secondary_y=True)


fig5.add_trace(
    go.Scatter(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['numVotes'], name='Number of Votes', mode='lines+markers'),
    secondary_y=True,)

fig5.add_trace(
    go.Scatter(x=top_10_by_revenue['originalTitle'], y=top_10_by_revenue['averageRating'], name='Average Rating', mode='lines+markers'),
    secondary_y=True,)


fig5.update_layout(xaxis_tickangle=30,
    title_text='Top 10 Films by Revenue, Profit, Number of Votes, and Average Rating',
    barmode='group',)

fig5.update_xaxes(title_text='Film Title')
fig5.update_yaxes(title_text='Revenue', secondary_y=False)
fig5.update_yaxes(title_text='Profit / Votes / Rating', secondary_y=True)




# In[40]:


import streamlit as st

st.header('Movie Finance Data')

with st.expander("Select Graphs to Display"):
    show_graph_1 = st.checkbox('Top 10 Films by Profit', True)
    show_graph_2 = st.checkbox('Top 10 Films by Revenue, Budget, and Profit', True)
    show_graph_3 = st.checkbox('Top 10 Films by Budget and Their Profits', True)
    show_graph_4 = st.checkbox('Top 10 Films by Revenue and Their Profits', True)
    show_graph_5 = st.checkbox('Top 10 Films by Revenue, Profit, Number of Votes, and Average Rating', True)

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




