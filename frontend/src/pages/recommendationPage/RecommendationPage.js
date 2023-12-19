import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './RecommendationPage.css';

const RecommendationPage = () => {
    const navigate = useNavigate();

    const handleNewClick = () => {
        // Redirect to the recommendation page
        navigate('/movies/content-base/recommendation');
    };

    const handleAccountClick = () => {
        // Redirect to the recommendation page
        navigate('/movies/collaborative-filtering/recommendation');
    };

    return (
        <div className="login-page">
            <h1>Welcome to Movie Recommendations</h1>
            <div className="login-buttons">
                <button onClick={handleNewClick}>New</button>
                <button onClick={handleAccountClick}>Already have account</button>
            </div>
        </div>
    );
};

export default RecommendationPage;
