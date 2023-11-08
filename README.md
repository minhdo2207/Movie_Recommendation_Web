# Movie_Recommendation_Web
Description: 
The project aims to build a movie recommendation web application which customizes its suggestions to each user's watch history and personal traits, based on how frequent they rate a movie. The recommendation system utilized in this project is a switching hybrid system which is a combination of Model-based Collaborative Filtering (CF) and Content-Based Recommendation(CB).

Input: 
User information(user preference) for newbie
UserId for existed user
Output: Movie recommendations
Algorithms:
Our system, switching a hybrid recommendation system is used to recommend movies to users. We define three cases for users, newbie, light user, and heavy user to apply this algorithm.



Model-based CF is a collaborative filtering algorithm that recommends movies based on the similarity between movies. It works by identifying movies that are similar to the ones the user has rated highly and then recommending those similar movies. Model-based CF performs better than user-based CF when dealing with sparse data.
Using K-means clustering to group similar users by several features such as occupation, age, gender can solve the Cold Start problem which occurs for new users.
Instead of using the original CB recommendation, which only applies to a one-to-one relationship, we propose a new approach that can estimate similarity between one movie and a group of movies.
Approach, tools used

Dataset
IMDB
Future Application:
The aim of this developing this application is to further improve user’s experience in the near future.Some of the benefits in the future is:
Cross-Platform Recommendations: As users increasingly access content across various platforms, recommendation systems will evolve to provide cross-platform suggestions. They may suggest a game, book, or music in addition to movies or TV shows.
Multilingual and Internationalization:Movie recommendation systems will need to cater to a more diverse audience. This means better support for multiple languages and recommendations for international content.
AI-Generated Content: AI may generate entirely new movies, shows, or scenes based on user preferences. Users could potentially request custom content.
