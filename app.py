import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

# -------------------- Load Environment Variables --------------------
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# -------------------- Streamlit Page Config --------------------
st.set_page_config(page_title="Netflix Recommender", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #141414;
            color: #ffffff;
        }
        .main {
            background-color: #141414;
        }
        h1 {
            color: #e50914;
        }
        .stButton button {
            background-color: #e50914;
            color: white;
            border: none;
            padding: 0.6em 1.5em;
            border-radius: 5px;
            font-size: 1em;
        }
        .stButton button:hover {
            background-color: #f40612;
        }
        .title-text {
            font-size: 2.5em;
            font-weight: bold;
            color: #e50914;
        }
        .recommendation-card {
            background-color: #1f1f1f;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- Check API Key --------------------
if not OMDB_API_KEY:
    st.error("🚨 OMDB API Key not found. Please create a `.env` file with `OMDB_API_KEY=your_key_here`")
    st.stop()

# -------------------- Poster Fetch Function --------------------
def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data["Response"] == "True" and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return f"https://via.placeholder.com/300x450?text={title.replace(' ', '+')}"
    except Exception as e:
        print("Poster fetch error:", e)
        return f"https://via.placeholder.com/300x450?text={title.replace(' ', '+')}"

# -------------------- Load & Process Dataset --------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r"dataset/netflix_titles.csv")
    df = df[['title', 'description', 'listed_in', 'type', 'date_added']]
    df.dropna(subset=['description'], inplace=True)
    df['listed_in'].fillna('', inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['release_year'] = df['date_added'].dt.year
    df['release_year'].fillna(0, inplace=True)
    df['release_year'] = df['release_year'].astype(int)
    df['content'] = df['description'] + ' ' + df['listed_in']
    return df

df = load_data()

@st.cache_resource
def compute_similarity(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['title'].str.lower()).drop_duplicates()
    return cosine_sim, indices

cosine_sim, indices = compute_similarity(df)

# -------------------- Recommendation Logic --------------------
def recommend(title, genre=None, year=None):
    title = title.lower()
    if title not in indices:
        return []

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]
    movie_indices = [i[0] for i in sim_scores]
    recommendations = df.iloc[movie_indices]

    if genre:
        recommendations = recommendations[recommendations['listed_in'].str.lower().str.contains(genre.lower())]
    if year:
        recommendations = recommendations[recommendations['release_year'] == year]

    return recommendations[['title', 'description']].head(10)

# -------------------- Streamlit UI --------------------
st.markdown('<h1 class="title-text">🍿 Netflix Recommender</h1>', unsafe_allow_html=True)
st.markdown("Get personalized recommendations based on your favorite Netflix title 🎥")

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    user_input = st.text_input("🔍 Enter a Netflix title (e.g., Narcos)", placeholder="Stranger Things")

with col2:
    genres = sorted(set(g for sublist in df['listed_in'].str.split(', ') for g in sublist))
    genre_filter = st.selectbox("🎭 Genre", [""] + genres)

with col3:
    years = sorted(df['release_year'].unique())
    year_filter = st.selectbox("📅 Year", [""] + years)

st.markdown("")

if st.button("🎬 Get Recommendations"):
    if not user_input:
        st.warning("⚠️ Please enter a title to search.")
    else:
        with st.spinner("🔎 Finding similar titles..."):
            results = recommend(user_input, genre_filter if genre_filter else None,
                                year_filter if year_filter else None)

        if len(results) > 0:
            st.success("✅ Here are your recommendations:")
            cols = st.columns(2)
            for i, row in results.iterrows():
                poster_url = fetch_poster(row['title'])
                with cols[i % 2]:
                    st.image(poster_url, width=200)
                    st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>🎞️ {row['title']}</h4>
                            <p style="font-size: 0.9em; color: #dddddd;">{row['description']}</p>
                            <a href="https://www.google.com/search?q={row['title'].replace(' ', '+')}+Netflix" target="_blank" style="color:#e50914;">🔗 Search on Google</a>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("😕 No recommendations found. Try a different title or filter.")
