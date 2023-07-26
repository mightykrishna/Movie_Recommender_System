import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
      

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
def recommend(movie):
    #we will fetch the movie index
    movie_index=movies[movies['title']==movie].index[0]
    #distances=similarity[movie_index]
    distances=sorted(list(enumerate(similarity[movie_index])),reverse=True,key=lambda x:x[1])
    recommend_movies=[]
    recommeded_movies_poster=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from API
        
        recommend_movies.append(movies.iloc[i[0]].title)
        recommeded_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies,recommeded_movies_poster
        
    

st.title('Movie Recommeder System')

selected_movie_name=st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values
)

if st.button('Show Recommendations'):
    names,posters=recommend(selected_movie_name)
    #st.write(selected_movie_name)
    
    col1, col2, col3 ,col4,col5= st.columns(5)

    with col1:
       st.text(names[0])
       st.image(posters[0])

    with col2:
       st.text(names[1])
       st.image(posters[1])

    with col3:
       st.text(names[2])
       st.image(posters[2])
    with col4:
       st.text(names[3])
       st.image(posters[3])

    with col5:
       st.text(names[4])
       st.image(posters[4])