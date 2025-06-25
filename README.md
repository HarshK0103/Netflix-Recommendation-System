# 🍿 Netflix Recommendation System

A smart, Netflix-style movie & show recommendation system built with **Streamlit**, **NLP (TF-IDF)**, and a curated Netflix dataset. The app features a clean UI, OMDb posters, genre/year filters, and Google search integration.

---

![Netflix UI Preview]() <!-- Replace with actual screenshot -->

---

## 🎯 Features

- 🔍 **Content-based Recommendations** using TF-IDF + Cosine Similarity
- 🎭 Filter by **Genre** and 📅 **Year**
- 🖼️ Automatically fetches **Posters via OMDb API**
- 🎬 Search links to Google for each title
- 🖤 Netflix-inspired **Dark Mode UI**
- 💡 Easy to deploy and extend

---

## 🧠 How It Works

1. Dataset is preprocessed using pandas.
2. Each movie/show is represented using TF-IDF on `description + genre`.
3. Cosine similarity calculates how close two titles are.
4. App displays 10 closest recommendations based on user’s input.
5. Posters are retrieved via OMDb API using title search.

---

## 🛠️ Tech Stack

| Tool           | Purpose                                 |
|----------------|------------------------------------------|
| Python         | Core programming language                |
| Streamlit      | Web interface                            |
| Pandas         | Data wrangling                           |
| Scikit-learn   | TF-IDF and Cosine Similarity             |
| OMDb API       | Poster retrieval                         |
| python-dotenv  | Secure key management                    |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/netflix-recommender.git
cd netflix-recommender
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have the file yet, create it with:

```bash
pip freeze > requirements.txt
```

---

## 🔐 Environment Setup

### 4. Get Your OMDb API Key

- Go to [https://www.omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)
- Choose the free plan and sign up.
- You'll get an API key via email.

### 5. Create `.env` File

In your project folder, create a file named `.env` and add:

```env
OMDB_API_KEY=your_omdb_api_key_here
```

### 6. Add `.env` to `.gitignore`

To prevent your key from being exposed on GitHub, add this line to `.gitignore`:

```
.env
```

> ✅ If `.gitignore` doesn't exist, create one and add `.env` to it.

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501)

---

## 📂 Project Structure

```
netflix-recommender/
├── app.py                 # Streamlit app
├── netflix_titles.csv     # Netflix dataset
├── .env                   # API key (hidden from Git)
├── .gitignore             # Ensures .env isn't uploaded
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 📊 Sample Output

| 🎬 Input Title      | ⭐ Top Recommendations                         |
|---------------------|-----------------------------------------------|
| Stranger Things     | The OA, Dark, Black Mirror, 13 Reasons Why    |
| Narcos              | Drug Lords, El Chapo, Breaking Bad            |
| The Crown           | The Royal House of Windsor, The Queen        |

---

## 🌐 Deployment

You can deploy this Streamlit app on:

### ✅ [Streamlit Cloud](https://share.streamlit.io/)
1. Push your code to GitHub
2. Go to Streamlit Cloud, sign in
3. Paste your GitHub repo URL
4. Set `app.py` as the entry file
5. Add your `OMDB_API_KEY` as a secret via "Advanced settings"

---

## ✨ Screenshots

<img src="" width="100%" alt="Netflix Recommender UI">

---

## 🤝 Contributing

Contributions and feedback are welcome!

To contribute:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

## 📧 Contact

**Harsh Karekar**

- 📬 hkarekar0103@gmail.com  
- 🔗 [LinkedIn](https://www.linkedin.com/in/harsh-karekar)

---

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
