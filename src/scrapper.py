import csv
import logging
import os
from datetime import datetime
from google_play_scraper import Sort, reviews

def scrape_reviews(app_id, bank_name, count=500):
    logging.info(f"🔄 Fetching reviews for {bank_name}...")

    try:
        results, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count
        )

        # Ensure the raw folder exists
        os.makedirs("data/raw", exist_ok=True)

        # Create timestamped filename without a subfolder
        safe_bank_name = bank_name.replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/raw/{safe_bank_name}_reviews_{timestamp}.csv"

        # Write to CSV
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['review_text', 'rating', 'date', 'bank_name', 'source'])
            writer.writeheader()

            for entry in results:
                writer.writerow({
                    'review_text': entry['content'],
                    'rating': entry['score'],
                    'date': entry['at'].strftime('%Y-%m-%d'),
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })

        logging.info(f"✅ Saved {len(results)} reviews to {filename}")
        return filename

    except Exception as e:
        logging.error(f"❌ Error while scraping {bank_name}: {e}")
        return None
