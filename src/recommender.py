import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class GameRecommender:
    def __init__(self, data_path=None):
        if data_path is None:
            # Default path relative to this script
            self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'steam_games.csv')
        else:
            self.data_path = data_path
            
        self.df = None
        self.similarity = None
        self._load_and_train()

    def _load_and_train(self):
        """Loads data, preprocesses it, and builds the TF-IDF similarity matrix."""
        # Load dataset
        self.df = pd.read_csv(self.data_path)
        
        # Preprocessing (Fill missing values)
        self.df['tags'] = self.df['tags'].fillna('')
        self.df['genre'] = self.df['genre'].fillna('')
        
        # Combine features
        self.df['features'] = self.df['genre'] + " " + self.df['tags']
        
        # Build TF-IDF Matrix
        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(self.df['features'])
        
        # Compute Cosine Similarity
        self.similarity = cosine_similarity(matrix)

    def recommend(self, game_name, top_n=5):
        """Core Recommendation Logic."""
        if game_name not in self.df['game_name'].values:
            return []

        # Find index of the game
        idx = self.df[self.df['game_name'] == game_name].index[0]
        
        # Get similarity scores for all games
        scores = list(enumerate(self.similarity[idx]))
        
        # Sort games based on similarity scores (descending)
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar games (excluding the game itself)
        top_games_indices = scores[1:top_n+1]
        
        # Return the actual game data for the recommendations
        recommended_games = []
        for i in top_games_indices:
            game_data = self.df.iloc[i[0]]
            recommended_games.append({
                'game_name': game_data['game_name'],
                'genre': game_data['genre'],
                'rating': game_data['rating'],
                'similarity_score': round(i[1] * 100, 2)
            })
            
        return recommended_games

    def get_trending_games(self, top_n=10):
        """Returns the top rated/popular games."""
        trending = self.df.sort_values(by=['rating', 'popularity'], ascending=[False, False]).head(top_n)
        return trending.to_dict('records')

    def get_all_game_names(self):
        """Utility to get all game names for the UI dropdown."""
        return self.df['game_name'].values

# Simple test if run directly
if __name__ == "__main__":
    recommender = GameRecommender()
    print("Test Recommendation for GTA V:")
    res = recommender.recommend("Grand Theft Auto V")
    for r in res:
        print(r['game_name'], "-", r['genre'])
