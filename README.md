# Movie_Recommendation_Web

## Description

The Movie Recommendation Web project aims to create a web application that provides personalized movie suggestions to users based on their watch history and personal traits. The recommendation system utilizes a switching hybrid approach, combining Model-based Collaborative Filtering (CF) and Content-Based Recommendation (CB) algorithms.

![Movie Recommendation](https://github.com/minhdo2207/Movie_Recommendation_Web/blob/main/image/IntroPic.png)

## Input

- **User Information (User Preference) for Newbie:** The system takes into account the preferences provided by new users.
- **User ID for Existing User:** Existing users can receive personalized recommendations based on their watch history and preferences.

## Output

- **Movie Recommendations:** The system provides tailored movie recommendations for each user.

## Algorithms

Our recommendation system uses a switching hybrid approach, categorizing users into three cases:

1. **Newbie:** For new users, K-means clustering is applied to group similar users based on features like occupation, age, and gender, solving the Cold Start problem.
2. **Light User:** Model-based Collaborative Filtering (CF) is employed to recommend movies based on the similarity between movies, identifying movies similar to ones the user has rated highly.
3. **Heavy User:** A combination of Model-based CF and a modified Content-Based Recommendation approach is used. This new approach estimates similarity between one movie and a group of movies, providing more accurate recommendations.

## Approach and Tools Used

- **Model-based Collaborative Filtering (CF):** Recommends movies based on the similarity between movies.
- **K-means Clustering:** Groups similar users by features such as occupation, age, and gender to address the Cold Start problem.
- **Content-Based Recommendation (CB):** Modified approach estimating similarity between one movie and a group of movies.

## Dataset

The dataset used in this project is sourced from IMDB.

## How to Use

1. Install the necessary dependencies.
2. Run the web application.
3. Input user preferences or existing user ID.
4. Receive personalized movie recommendations.

## Contributing

Feel free to contribute by opening issues or submitting pull requests.

## License

This project is licensed under the HUST



