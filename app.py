import streamlit as st
import pickle
import base64
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=231dc9f7275e1d5c5b358bb5bb51a2de"
                            .format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

imported_movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(imported_movies)


def recommend(movie):
  m_index = movies[movies['title'] == movie].index[0]
  distances = similarity[m_index]
  movies_list = sorted(list(enumerate(distances)),reverse= True, key=lambda x:x[1])[1:6]

  recommended_movies = []
  recommended_movies_posters= []

  for i in movies_list:
    movie_id = movies.iloc[i[0]].movie_id
    recommended_movies.append(movies.iloc[i[0]].title)
    #fetch movie poster
    recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies, recommended_movies_posters



#bg image
st.markdown(
    "<h1><span style='color: #d43122;'>Cinema</span> <span style='color: #f5f4e4;'>Recommendation</span></h1>",
    unsafe_allow_html=True
)


imported_movies = imported_movies['title'].values


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    bg_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
    }}
    </style>
    """

    st.markdown(bg_image, unsafe_allow_html=True)


# Path to your local image
local_image_path = "pos4.png"

# Apply the background
add_bg_from_local(local_image_path)



# Styled label using HTML and markdown
st.markdown(
    "<p style='color:#f5f4e4; font-size:20px;'>🍿 Tell us what you like to watch!</p>",
    unsafe_allow_html=True
)

# Selectbox with no label
selected_movie = st.selectbox(
    "",
    options=imported_movies,
    index=None,
)






if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(
            f"<p style='color:#f5f4e4;'>{recommended_movie_names[0]}</p>",
            unsafe_allow_html=True
        )
        st.image(recommended_movie_posters[0])
    with col2:
        st.markdown(
            f"<p style='color:#f5f4e4;'>{recommended_movie_names[1]}</p>",
            unsafe_allow_html=True
        )
        st.image(recommended_movie_posters[1])

    with col3:
        st.markdown(
            f"<p style='color:#f5f4e4;'>{recommended_movie_names[2]}</p>",
            unsafe_allow_html=True
        )
        st.image(recommended_movie_posters[2])
    with col4:
        st.markdown(
            f"<p style='color:#f5f4e4;'>{recommended_movie_names[3]}</p>",
            unsafe_allow_html=True
        )
        st.image(recommended_movie_posters[3])
    with col5:
        st.markdown(
            f"<p style='color:#f5f4e4;'>{recommended_movie_names[4]}</p>",
            unsafe_allow_html=True
        )
        st.image(recommended_movie_posters[4])
