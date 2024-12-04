import pickle
import pandas as pd
import streamlit as st
import requests
import base64


def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .header-box {{
            padding: 10px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 1.0); /* Semi-transparent white */
            text-align: center;
            color: #000000; /* Black text color */
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        .input-box {{
            padding: 10px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 1.0); /* Semi-transparent white */
            color: #000000; /* Black text color */
            margin-bottom: 20px;
        }}
        .recommendation-box {{
            border: 2px solid #FFFFFF;  /* White border */
            padding: 10px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 1.0); /* Semi-transparent background */
            text-align: center;
            color: #000000; /* Black text color */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Set background image
set_background("img.png")


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except (requests.exceptions.RequestException, KeyError):
        # Handle errors, return a placeholder image URL or a message
        return "https://via.placeholder.com/500x750?text=Image+Not+Available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Display header with custom style
st.markdown('<div class="header-box">MOVIE RECOMMENDER SYSTEM</div>', unsafe_allow_html=True)

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Display input box with custom style
st.markdown('<div class="input-box">Enter a movie name:</div>', unsafe_allow_html=True)
selected_movie_name = st.selectbox('', movies['title'].values)

# Recommendation button and display
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(
                f"""
                <div class="recommendation-box">
                    <p>{names[idx]}</p>
                    <img src="{posters[idx]}" width="100%" />
                </div>
                """,
                unsafe_allow_html=True
            )
