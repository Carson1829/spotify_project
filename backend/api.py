from flask import Flask, request, jsonify
from flask_cors import CORS
from data import search_songs, predict_genre
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_songs(query)
    return jsonify(results)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    app.logger.info(f'Received data: {data}')
    track = data.get('track')
    artist = data.get('artist')
    predicted_genres = predict_genre(track, artist)
    app.logger.info(f'Predicted genre: {predicted_genres}')
    
    return jsonify({'genres': predicted_genres})

if __name__ == '__main__':
    app.run(debug=True)
