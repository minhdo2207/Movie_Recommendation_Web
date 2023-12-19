// RecommendationPage.js

import React, { useState } from 'react';
import axios from 'axios';
import './RecommendationPage.css';

const RecommendationPage = () => {
    const [movieTitle, setMovieTitle] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleRecommendation = async () => {
        try {
            setLoading(true);

            const response = await axios.post('http://localhost:5000/api/content-base-recommend', { movie_title: movieTitle });
            const movieTitles = response.data.recommendations;

            const movieDetailsPromises = movieTitles.map(async (title) => {
                const tmdbResponse = await axios.get(`https://api.themoviedb.org/3/search/movie`, {
                    params: {
                        api_key: '4e44d9029b1270a757cddc766a1bcb63',
                        query: title
                    }
                });

                const movieDetails = tmdbResponse.data.results[0];
                return {
                    original_title: movieDetails.original_title,
                    releaseDate: movieDetails.release_date,
                    overview: movieDetails.overview,
                    posterPath: movieDetails.poster_path
                };
            });

            const movieDetails = await Promise.all(movieDetailsPromises);
            setRecommendations(movieDetails);
        } catch (error) {
            setError('Error fetching recommendations');
            console.error('Error fetching recommendations:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="recommendation-page">
            <div className="search-bar">
                <input type="text" value={movieTitle} onChange={(e) => setMovieTitle(e.target.value)} />
                <button onClick={handleRecommendation} disabled={loading}>
                    {loading ? 'Loading...' : 'Get Recommendations'}
                </button>
            </div>

            <div>
                {error && <p className="error-message">{error}</p>}

                <h2>Recommended Movies:</h2>
                <div className="movie-list">
                    {recommendations.map((movie, index) => (
                        <div key={index} className="movie-container">
                            <img src={`https://image.tmdb.org/t/p/original${movie ? movie.posterPath : ''}`} alt={movie ? movie.original_title : ''} />
                            <div className="movie-details">
                                <h3>{movie ? movie.original_title : ''}</h3>
                                <p>Release Date: {movie ? movie.releaseDate : ''}</p>
                                <p>{movie ? movie.overview.slice(0, 118) + "..." : ""}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default RecommendationPage;
