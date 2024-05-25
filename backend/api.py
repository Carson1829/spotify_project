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

if __name__ == '__main__':
    app.run(debug=True)
