from flask import Flask, request, jsonify
from flask_cors import CORS
from data import search_songs, get_track_info
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
    predicted_genre = predict_genre(track, artist)
    app.logger.info(f'Predicted genre: {predicted_genre}')
    
    return jsonify({'genre': predicted_genre})

def predict_genre(track, artist):
    # Replace with machine learning model that would get called for a prediction
    test = get_track_info(track, artist)
    return test  # test genre


if __name__ == '__main__':
    app.run(debug=True)
