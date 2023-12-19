import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Header from './components/header/Header';
import Home from './pages/home/home';
import MovieList from './components/movieList/movieList';
import Movie from './pages/movieDetail/movie';
import RecommendationPage from './pages/recommendationPage/RecommendationPage';  // Make sure to import the correct path for RecommendationPage
import ContentRecommendationPage from './pages/contentBaseRecommendation/ContentRecommendationPage'
import CollaborativeRecommendationPage from './pages/collaborativeRecommendation/CollaborativeRecommendationPage'

function App() {
  return (
    <div className="App">
        <Router>
          <Header />
            <Routes>
                <Route index element={<Home />}></Route>
                <Route path="movie/:id" element={<Movie />}></Route>
                <Route path="movies/:type" element={<MovieList />}></Route>
                <Route path="/movies/recommendation" element={<RecommendationPage />} />  
                <Route path="/movies/content-base/recommendation" element={<ContentRecommendationPage />} />  
                <Route path="/movies/collaborative-filtering/recommendation" element={<CollaborativeRecommendationPage />} />  
                <Route path="/*" element={<h1>Error Page</h1>}></Route>
            </Routes>
        </Router>
    </div>
  );
}

export default App;
