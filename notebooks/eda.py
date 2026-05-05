import pandas as pd
import os

def run_eda():
    # Load the data
    # Navigate relative to the script location (notebooks folder -> root -> data)
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'steam_games.csv')
    
    if not os.path.exists(data_path):
        print(f"Error: Could not find dataset at {data_path}")
        return

    print("Loading Dataset...\n")
    df = pd.read_csv(data_path)
    
    print("--- HEAD (First 5 Rows) ---")
    print(df.head())
    print("\n")
    
    print("--- INFO (Column Types & Non-Null Counts) ---")
    print(df.info())
    print("\n")
    
    print("--- CHECKING MISSING VALUES ---")
    print(df.isnull().sum())
    print("\n")
    
    # 🧹 STEP 4: Data Preprocessing Demo
    print("--- PREPROCESSING DEMO ---")
    # Handle missing tags/genres if any
    df['tags'] = df['tags'].fillna('')
    df['genre'] = df['genre'].fillna('')
    
    # Combine features
    df['features'] = df['genre'] + " " + df['tags']
    print("\nCombined Features Column Created:")
    print(df[['game_name', 'features']].head())

if __name__ == "__main__":
    run_eda()
