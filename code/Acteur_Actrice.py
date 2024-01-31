#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from datetime import datetime
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# In[67]:


movies_filtered = pd.read_csv(r"C:/Users/User/Desktop/csv data/movies_filtered.zip",compression = 'zip', low_memory=False)
movies_filtered1 = movies_filtered[['tconst', 'averageRating', 'originalTitle', 'numVotes', 'ranking']]


# In[68]:


title_principals = pd.read_csv(r"C:/Users/User/Desktop/csv data/principlals_filtered.zip", compression = 'zip', low_memory=False)
title_principals1 = title_principals[['tconst', 'nconst', 'category']]


# In[69]:


name_basics = pd.read_csv(r"C:/Users/User/Desktop/csv data/names_filtered.zip", compression = 'zip', low_memory=False)
name_basics1 = name_basics[['nconst', 'primaryName']]


# In[70]:


merged_data = pd.merge(movies_filtered1, title_principals1, on='tconst', how='left')


# In[71]:


merge_final = pd.merge(merged_data, name_basics1, on='nconst', how='left')


# In[72]:


actors_and_actresses = merge_final[(merge_final['category'] == "actor") | (merge_final['category'] == "actress")]


# In[73]:


actors_and_actresses = actors_and_actresses.head(20000)


# In[74]:


actors_and_actresses = actors_and_actresses.groupby(['primaryName', 'category'])['tconst'].count().reset_index()


# In[75]:


top_performers = actors_and_actresses.sort_values(by='tconst', ascending=False).groupby('category').head(10)


# In[77]:


fig1 = px.bar(top_performers, x='primaryName', y='tconst', color='category',
             labels={'primaryName': 'Nom', 'tconst': 'Nombre de films', 'category': 'Genre'},
             title='Top 10 Acteurs et Actrices dans le top 10% des meilleurs films')


# In[78]:


movies_filtered2 = movies_filtered[['tconst','originalTitle','revenue','budget']]


# In[79]:


title_principals2 = title_principals[['tconst', 'nconst', 'category']]


# In[80]:


name_basics2 = name_basics[['nconst', 'primaryName']]


# In[81]:


merged_data2 = pd.merge(movies_filtered2, title_principals2, on='tconst', how='left')


# In[82]:


merge_final1 = pd.merge(merged_data2, name_basics2, on='nconst', how='left')


# In[83]:


actors_and_actresses1 = merge_final1[(merge_final1['category'] == "actor") | (merge_final1['category'] == "actress")]


# In[84]:


actors_and_actresses1 = actors_and_actresses1[actors_and_actresses1['revenue'] > 0]


# In[85]:


actors_and_actresses1 = actors_and_actresses1[actors_and_actresses1['budget'] > 0]


# In[87]:


actors_and_actresses1 = actors_and_actresses1.head(20000)


# In[88]:


revenue_max = actors_and_actresses1.groupby(['category', 'primaryName'])['revenue'].sum().reset_index()
top_10_per_category = revenue_max.groupby('category').apply(lambda x: x.nlargest(10, 'revenue')).reset_index(drop=True)


# In[89]:


revenue_max = revenue_max.nlargest(10, 'revenue')


# In[90]:


fig2 = px.bar(revenue_max, x='primaryName', y='revenue', color='category',
             labels={'primaryName': 'Nom', 'revenue': 'revenue'},
             title='Top 10 Acteurs avec le Plus de Chiffre d\'Affaires')


# In[27]:


title_principals3 = title_principals[['tconst', 'nconst', 'category']]


# In[28]:


name_basics3 = name_basics[['nconst', 'primaryName']]


# In[29]:


merged_data3 = pd.merge(movies_filtered, title_principals3, on='tconst', how='left')


# In[30]:


merge_final3 = pd.merge(merged_data3, name_basics3, on='nconst', how='left')


# In[31]:


merge_final3 = merge_final3[merge_final3['category'] == 'director']


# In[32]:


director = merge_final3.head(1000)


# In[33]:


director_popularity = director.groupby('primaryName')['numVotes'].sum().reset_index()
director_popularity = director_popularity.sort_values('numVotes', ascending = False)


# In[34]:


director_popularity = director_popularity.nlargest(10, 'numVotes')


# In[35]:


fig3 = px.bar(director_popularity, x='primaryName', y='numVotes',
             labels={'primaryName': 'Nom', 'numVotes': 'nombre de vote'},
             title='Classement des réalisateurs en fonction de la popularité')


# In[36]:


movies_filtered4 = movies_filtered[['tconst', 'originalTitle', 'revenue', 'ranking']]


# In[37]:


title_principal4 = title_principals[['tconst', 'nconst', 'category']]


# In[38]:


name_basics4 = name_basics[['nconst', 'primaryName']]


# In[39]:


merged_data4 = pd.merge(movies_filtered4, title_principal4, on='tconst', how='left')


# In[40]:


merge_final4 = pd.merge(merged_data4, name_basics4, on='nconst', how='left')


# In[41]:


merge_final4 = merge_final4[merge_final4['revenue'] > 0]


# In[42]:


writer = merge_final4[(merge_final4['category'] == "writer")]


# In[43]:


top_writer = writer.groupby('primaryName')['revenue'].sum().reset_index()
top_writer = top_writer.sort_values('revenue', ascending = False)


# In[44]:


top_writer = top_writer.nlargest(10, 'revenue')


# In[45]:


fig4 = px.bar(top_writer, x='primaryName', y='revenue',
             labels={'primaryName': 'Nom', 'revenue': 'revenue'},
             title='Top 10 writer avec le Plus de Chiffre d\'Affaires')


# In[45]:


import streamlit as st
st.header('Acteurs/Actrices/directeur/écrivant')

with st.expander("Select Graphs to Display"):
    show_graph_1 = st.checkbox('Top 10 Acteurs et Actrices dans le top 10% des meilleurs films', True)
    show_graph_2 = st.checkbox('Top 10 Acteurs avec le Plus de Chiffre d\'Affaires', True)
    show_graph_3 = st.checkbox('Classement des réalisateurs en fonction de la popularité', True)
    show_graph_4 = st.checkbox('Top 10 writer avec le Plus de Chiffre d\'Affaires', True)

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




