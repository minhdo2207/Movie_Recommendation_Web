from flask import Flask, request, jsonify
from content_based_recommender import contents_based_recommender
from collaborative_filtering_recommender import item_based_recommender
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/api/content-base-recommend', methods=['POST'])
def content_based_recommend_movies():
    try:
        data = request.get_json()
        movie_title = data.get('movie_title')

        # Get recommended movies as a list of titles
        recommended_movies = contents_based_recommender(movie_title, num_of_recomm=10)

        return jsonify({'recommendations': recommended_movies})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/api/collaborative-filtering-recommend', methods=['POST'])
def collaborative_filteringl_recommend_movies():
    try:
        data = request.get_json()
        userId = data.get('userId')

        # Get recommended movies as a list of titles
        recommended_movies = item_based_recommender(userId)

        return jsonify({'recommendations': recommended_movies})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
