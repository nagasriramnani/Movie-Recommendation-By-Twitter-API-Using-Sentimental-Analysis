from flask import Flask, render_template, request
import engine as re

# Replace 'your_tmdb_api_key' with your actual TMDb API key
tmdb_api_key = '80569fb891a2ad938180e54b007066c4'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommended_movies = re.recommend_movies(movie_title, tmdb_api_key)
    return render_template('index.html', recommended_movies=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)
