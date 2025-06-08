import pandas as pd

import os

def clean_reviews(csv_filepath, output_filepath=None):
    # Load CSV
    df = pd.read_csv(csv_filepath)

    # 1. Remove duplicates based on review_text, date, bank_name
    df = df.drop_duplicates(subset=['review_text', 'date', 'bank_name'])

    # 2. Handle missing data
    df = df.dropna(subset=['review_text', 'rating', 'date'])

    # Remove emojis from review_text
    # df['review_text'] = df['review_text'].astype(str).apply(remove_emojis).str.strip()

    # Convert rating to integer
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df = df.dropna(subset=['rating'])
    df['rating'] = df['rating'].astype(int)

    # Normalize date format (to yyyy-mm-dd)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    # Prepare output filename inside data/cleaned/
    if output_filepath is None:
        # Extract bank name from input filename
        basename = os.path.basename(csv_filepath)  # e.g. 'cbe_reviews_20250608_123456.csv'
        # You might want to strip everything after first underscore or use a cleaner approach:
        bank_name = basename.split('_')[0].lower()  # e.g. 'cbe'
        output_folder = 'data/cleaned'
        os.makedirs(output_folder, exist_ok=True)
        output_filepath = os.path.join(output_folder, f"{bank_name}.csv")

    # Save cleaned data
    df.to_csv(output_filepath, index=False)

    print(f"Cleaned data saved to {output_filepath}")

    return df

clean_reviews('data/raw/Bank_of_Abyssinia_reviews_20250608_212746.csv')
clean_reviews('data/raw/Commercial_Bank_of_Ethiopia_reviews_20250608_211533.csv')
clean_reviews('data/raw/Dashen_Bank_reviews_20250608_211530.csv')



