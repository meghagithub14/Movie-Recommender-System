import pandas as pd
import requests
import streamlit as st
import pickle

API_KEY = "641bdccf42a8e73cc3d0b1be8233cd61"

def fetch_poster(movie_id):
    """
    Fetch the TMDb poster for a given movie_id.
    Falls back to a placeholder if anything goes wrong.
    """
    url    = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": API_KEY}
    try:
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        # network issue or bad status code
        print(f"[fetch_poster] error for {movie_id}:", e)
        return "https://via.placeholder.com/185x278?text=No+Image"

    poster_path = data.get("poster_path")

    return f"https://image.tmdb.org/t/p/w185{poster_path}"

def recommend(movie):
    idx       = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similar[idx]))
    # sort by similarity score, skip the first (itself), take next 5
    top5      = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    titles  = []
    posters = []
    for i, _ in top5:
        m_id = movies.iloc[i].movie_id
        titles.append(movies.iloc[i].title)
        posters.append(fetch_poster(m_id))

    return titles, posters


# ──────── load your data ─────────────────────────────────────────────────────
movies  = pd.DataFrame(pickle.load(open('movie_dict.pkl','rb')))
similar = pickle.load(open('similar.pkl','rb'))

# ──────── Streamlit UI ───────────────────────────────────────────────────────
st.title('Movie Recommendation System')

selected_movie = st.selectbox('Select a movie', movies['title'].values)
if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)

