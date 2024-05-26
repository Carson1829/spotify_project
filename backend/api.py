from flask import Flask, request, jsonify
from flask_cors import CORS
from data import search_songs

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
    
    # Here you would call your machine learning model with the track and artist
    # For this example, let's assume you have a function called `predict_genre`
    predicted_genre = predict_genre(track, artist)
    app.logger.info(f'Predicted genre: {predicted_genre}')
    
    return jsonify({'genre': predicted_genre})

def predict_genre(track, artist):
    # Placeholder function for running your machine learning model
    # Replace this with your actual model prediction logic
    return "Rock"  # Example genre

if __name__ == '__main__':
    app.run(debug=True)
