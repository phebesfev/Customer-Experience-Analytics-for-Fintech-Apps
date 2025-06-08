import json
import logging
import os
import sys


# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scrapper import scrape_reviews  # ✅ FIXED: 'scrapper' → 'scraper'


# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Setup logging
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load app IDs from config
try:
    with open('configs/banks.json', 'r', encoding='utf-8') as f:
        app_ids = json.load(f)
    logging.info("📁 Successfully loaded bank config.")
except Exception as e:
    logging.error(f"❌ Failed to load banks.json: {e}")
    raise

# Run scraping for each bank
for bank_name, app_id in app_ids.items():
    logging.info(f"🚀 Starting scrape for {bank_name}")
    scrape_reviews(app_id, bank_name, count=500)

