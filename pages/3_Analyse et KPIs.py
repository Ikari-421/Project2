import streamlit as st
import plotly.express as px
import pandas as pd


st.set_page_config(
    page_title="Analyse et KPIs",
    page_icon="📈",
    layout="wide")

# import matplotlib
# import plotly
# import sklearn
# import pandas
# import streamlit

# st.title('pandas=='+pandas.__version__)
# st.title('streamlit=='+streamlit.__version__)
# st.title('sklearn=='+sklearn.__version__)
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


#
# ALL FUNCTIONS 
#
                    
                    
def production_charts(filtered_df):

        background_color = "#f9f9f9"
        text_color = "DarkSlateGrey"
        color_chart_1 = "RoyalBlue"
        dict_title = {'y':0.9, 'x':0.5,
                      'xanchor': 'center',
                      'yanchor': 'top',
                      'font': dict(color=text_color)
                      }


        filtered_df['production_companies_name'] = filtered_df['production_companies_name'].apply(
            lambda x: x if isinstance(x, list) else x.replace('[', '').replace(']', '').replace("'", '').split(','))
        
        exploded_df = filtered_df.explode('production_companies_name')

        cleaned_movies = exploded_df[exploded_df['production_companies_name'] != '']

        cleaned_movies.loc[:, 'production_companies_name'] = cleaned_movies['production_companies_name'].str.lstrip()

        top_5000=cleaned_movies.head(5000)

        company_movie_counts = cleaned_movies.groupby('production_companies_name')['tconst'].nunique()

        top_10_companies = company_movie_counts.sort_values(ascending=False).head(10)
        top_10_companies_df = top_10_companies.reset_index()
        top_10_companies_df.columns = ['Production Company', 'Number of Movies']

        fig1 = px.bar(top_10_companies_df, 
             x='Production Company', 
             y='Number of Movies',
             color_discrete_sequence=[color_chart_1])
        dict_title["text"] = "Top 10 Production Companies by Number of Movies"
        fig1.update_layout(
            title=dict_title,
            xaxis_title=None,
            yaxis_title=None,
            xaxis_tickangle=30,
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            font=dict(color=text_color))

        fig1.update_xaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig1.update_yaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))

        top_1000 = cleaned_movies.head(1000)
        company_movie_counts2 = top_1000.groupby('production_companies_name')['tconst'].nunique()
        top_10_companies2 = company_movie_counts2.sort_values(ascending=False).head(10)
        top_10_companies_df2 = top_10_companies.reset_index()
        top_10_companies_df2.columns = ['Production Company', 'Number of Movies']

        fig2 = px.bar(top_10_companies2, 
            title='Top 10 Production Companies in Top 1000 Highest Ranked Films',
            labels={'value': 'Number of Films', 'index': 'Production Company'},
            color_discrete_sequence=[color_chart_1]
        )
        dict_title["text"] = "Top 10 Production Companies in Top 1000 Highest Ranked Films"
        fig2.update_layout(
            title = dict_title,
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            font=dict(color=text_color),
            xaxis_title=None,
            yaxis_title=None
        )
        fig2.update_xaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig2.update_yaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig2.update_layout(showlegend=False)

        top_5000['Profit'] = top_5000['revenue'] - top_5000['budget']
        total_profit_by_company = top_5000.groupby('production_companies_name')['Profit'].sum()

        most_successful_companies = total_profit_by_company.sort_values(ascending=False).head(10)
        most_successful_companies_df = most_successful_companies.reset_index()
        most_successful_companies_df.columns = ['Production Company', 'Total Profit']


        fig3 = px.bar(most_successful_companies_df, 
                    y='Production Company', 
                    x='Total Profit',
                    color_discrete_sequence=[color_chart_1], 
                    orientation='h',)
        
        dict_title["text"] = "Top 10 Most Successful Production Companies by Profit"
        fig3.update_layout(
            title = dict_title,
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            font=dict(color=text_color),
            xaxis_title=None,
            yaxis_title=None
        )

        fig3.update_xaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig3.update_yaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))

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
                    color_discrete_sequence=[color_chart_1])
        
        dict_title["text"] = "Top 10 Production Companies by Average Profit per Film (Min 10 Films)"
        fig4.update_layout(
            title = dict_title,
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            font=dict(color=text_color),
            xaxis_title=None,
            yaxis_title=None)

        fig4.update_xaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig4.update_yaxes(title_font=dict(color=text_color), tickfont=dict(color=text_color))

        companies_per_year = cleaned_movies.groupby('startYear')['production_companies_name'].nunique().reset_index()

        fig5 = px.line(
            companies_per_year, 
            x='startYear', 
            y='production_companies_name', 
            labels={'startYear': 'Year', 'production_companies_name': 'Number of Production Companies'},
            title='Number of Production Companies Over the Years',
            color_discrete_sequence=[color_chart_1])

        dict_title["text"] = "Number of Production Companies Over the Years"
        fig5.update_layout(
            title = dict_title,
            plot_bgcolor=background_color,
            paper_bgcolor=background_color,
            font=dict(color=text_color),
            xaxis_title=None,
            yaxis_title=None)

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

def finance_charts(filtered_df):
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        filtered_df['Profit'] = filtered_df['revenue'] - filtered_df['budget']

        top_10_profitable_movies = filtered_df.sort_values(by='revenue', ascending=False).head(10)

        fig1 = px.bar(top_10_profitable_movies, x='originalTitle', y='Profit',
                    title='Top 10 Films by Profit',
                    labels={'originalTitle': 'Film Title', 'Profit': 'Profit'},
                    color='Profit')

        fig1.update_layout(xaxis_tickangle=30,
            xaxis_title='Film Title',
            yaxis_title='Profit')

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



        top_10_by_budget = filtered_df.sort_values(by='budget', ascending=False).iloc[1:11]


        fig3 = px.bar(top_10_by_budget, x='originalTitle', y=['budget', 'Profit'],
                            title='Top 10 Films by Budget and Their Profits',
                            labels={'originalTitle': 'Film Title', 'value': 'Amount', 'variable': 'Type'})

        fig3.update_layout(xaxis_tickangle=30,
            xaxis_title='Film Title',
            yaxis_title='Amount')



        top_10_by_revenue = filtered_df.sort_values(by='revenue', ascending=False).head(10)

        fig4 = px.bar(top_10_by_revenue, x='originalTitle', y=['revenue', 'Profit'],
                            title='Top 10 Films by Revenue and Their Profits',
                            labels={'originalTitle': 'Film Title', 'value': 'Amount', 'variable': 'Type'})

        fig4.update_layout(xaxis_tickangle=30,
            xaxis_title='Film Title',
            yaxis_title='Amount')


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

def actors_charts(movies_filtered, title_principals, name_basics):
        movies_filtered1 = movies_filtered[['tconst', 'averageRating', 'originalTitle', 'numVotes', 'ranking_1']]
        title_principals1 = title_principals[['tconst', 'nconst', 'category']]
        name_basics1 = name_basics[['nconst', 'primaryName']]

        merged_data = pd.merge(movies_filtered1, title_principals1, on='tconst', how='left')

        merge_final = pd.merge(merged_data, name_basics1, on='nconst', how='left')

        actors_and_actresses = merge_final[(merge_final['category'] == "actor") | (merge_final['category'] == "actress")]

        actors_and_actresses = actors_and_actresses.head(20000)

        actors_and_actresses = actors_and_actresses.groupby(['primaryName', 'category'])['tconst'].count().reset_index()

        top_performers = actors_and_actresses.sort_values(by='tconst', ascending=False).groupby('category').head(10)

        fig1 = px.bar(top_performers, x='primaryName', y='tconst', color='category',
                    labels={'primaryName': 'Nom', 'tconst': 'Nombre de films', 'category': 'Genre'},
                    title='Top 10 Acteurs et Actrices dans le top 10% des meilleurs films')

        movies_filtered2 = movies_filtered[['tconst','originalTitle','revenue','budget']]

        title_principals2 = title_principals[['tconst', 'nconst', 'category']]


        name_basics2 = name_basics[['nconst', 'primaryName']]

        merged_data2 = pd.merge(movies_filtered2, title_principals2, on='tconst', how='left')

        merge_final1 = pd.merge(merged_data2, name_basics2, on='nconst', how='left')

        actors_and_actresses1 = merge_final1[(merge_final1['category'] == "actor") | (merge_final1['category'] == "actress")]

        actors_and_actresses1 = actors_and_actresses1[actors_and_actresses1['revenue'] > 0]

        actors_and_actresses1 = actors_and_actresses1[actors_and_actresses1['budget'] > 0]

        actors_and_actresses1 = actors_and_actresses1.head(20000)

        revenue_max = actors_and_actresses1.groupby(['category', 'primaryName'])['revenue'].sum().reset_index()
        top_10_per_category = revenue_max.groupby('category').apply(lambda x: x.nlargest(10, 'revenue')).reset_index(drop=True)

        revenue_max = revenue_max.nlargest(10, 'revenue')

        fig2 = px.bar(revenue_max, x='primaryName', y='revenue', color='category',
                    labels={'primaryName': 'Nom', 'revenue': 'revenue'},
                    title='Top 10 Acteurs avec le Plus de Chiffre d\'Affaires')
        
        title_principals3 = title_principals[['tconst', 'nconst', 'category']]

        name_basics3 = name_basics[['nconst', 'primaryName']]

        merged_data3 = pd.merge(movies_filtered, title_principals3, on='tconst', how='left')

        merge_final3 = pd.merge(merged_data3, name_basics3, on='nconst', how='left')

        merge_final3 = merge_final3[merge_final3['category'] == 'director']

        director = merge_final3.head(1000)

        director_popularity = director.groupby('primaryName')['numVotes'].sum().reset_index()

        director_popularity = director_popularity.sort_values('numVotes', ascending = False)

        director_popularity = director_popularity.nlargest(10, 'numVotes')

        fig3 = px.bar(director_popularity, x='primaryName', y='numVotes',
                    labels={'primaryName': 'Nom', 'numVotes': 'nombre de vote'},
                    title='Classement des réalisateurs en fonction de la popularité')

        movies_filtered4 = movies_filtered[['tconst', 'originalTitle', 'revenue', 'ranking_1']]

        title_principal4 = title_principals[['tconst', 'nconst', 'category']]

        name_basics4 = name_basics[['nconst', 'primaryName']]


        merged_data4 = pd.merge(movies_filtered4, title_principal4, on='tconst', how='left')


        merge_final4 = pd.merge(merged_data4, name_basics4, on='nconst', how='left')

        merge_final4 = merge_final4[merge_final4['revenue'] > 0]

        writer = merge_final4[(merge_final4['category'] == "writer")]

        top_writer = writer.groupby('primaryName')['revenue'].sum().reset_index()
        top_writer = top_writer.sort_values('revenue', ascending = False)

        top_writer = top_writer.nlargest(10, 'revenue')

        fig4 = px.bar(top_writer, x='primaryName', y='revenue',
                    labels={'primaryName': 'Nom', 'revenue': 'revenue'},
                    title='Top 10 writer avec le Plus de Chiffre d\'Affaires')

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

def genres_charts(filtered_df):

        filtered_df['genres'] = filtered_df['genres'].astype(str)
        filtered_df['genres'] = filtered_df['genres'].str.split(',')
        exploded_df = filtered_df.explode('genres')

        exploded_df['Profit'] = exploded_df['revenue'] - exploded_df['budget']


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
        finance_charts(filtered_df)

    with tab3:
        st.markdown("<h3 class='title-tab'>Production companies</h3>", unsafe_allow_html=True)
        production_charts(filtered_df)

    with tab4:
        st.markdown("<h3 class='title-tab'>Acteurs / directeur / écrivant</h3>", unsafe_allow_html=True)
        actors_charts(csv_movies, title_principals, name_basics)

    with tab5:
        st.markdown("<h3 class='title-tab'>Genres</h3>", unsafe_allow_html=True)
        genres_charts(filtered_df)
