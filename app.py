import streamlit as st
import pickle
import pandas as pd
import requests
import random

# Set page title and favicon
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# Define function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1beb542dbe844f60f6ad8c26a7a1191b&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Define function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

# Title
st.title('🎬 Movie Recommender System')
st.markdown("""<style>.css-145kmoq {margin-top: -30px;}</style>""", unsafe_allow_html=True)

# Selectbox for movie selection
selected_movie_name = st.selectbox(
    "🍿 Type or select a movie from the dropdown",
    movies['title'].values
)

# Button to show recommendations
if st.button('🔍 Show Recommendations'):
    names, posters = recommend(selected_movie_name)

    # Display recommendations with columns
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i, (name, poster) in enumerate(zip(names, posters)):
        with cols[i]:
            st.write(f"**{name}**")
            st.image(poster, use_column_width=True)

# Cool message
cool_messages = [
    "This is cool! 🚀🎉",
    "Watch movies and chill! 🍿😎",
    "Discover new favorites! 🌟🎬",
    "Movie magic awaits! ✨🎥",
    "Lights, camera, action! 🎬🍿",
    "Get ready to be entertained! 🤩🍿"
]

# Use JavaScript to display cool message for 2 seconds
cool_message = random.choice(cool_messages)
st.markdown(
    f"""
    <div id="cool-message" class="cool-message">{cool_message}</div>
    <script>
    setTimeout(function() {{
        var coolMessage = document.getElementById('cool-message');
        coolMessage.style.display = 'none';
    }}, 2000);
    </script>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(135deg, #833ab4, #fd1d1d);
        padding: 10px 0;
        text-align: center;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.7);
        z-index: 200;
    }
    .footer div {
        display: inline-block;
        margin-right: 20px;
        font-size: 14px; /* Adjust font size for better visibility */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display footer messages with unique symbols
st.markdown('<div class="footer"><div class="center-message">Escape Reality, Watch Movies! 🚀🎥</div><div class="right-message">Lights Off, Movie On! 🎥🍿</div><div class="left-message">Indulge in cinematic adventures! 🌟🎬</div><div class="center-message">Dive into a world of entertainment! 🚀🎉</div><div class="right-message">Movie Marathon Time! 🎥🍿</div></div>', unsafe_allow_html=True)
