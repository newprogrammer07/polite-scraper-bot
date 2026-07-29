# The Polite Scraper - Week 5 Assignment

## Overview
This project is the Week 5 assignment for the Backend AI Engineering track. The goal is to build a robust, polite data-gathering pipeline (fetch → parse → extract → clean → structure). 

**Note on Target Site Selection:** 
Since a specific target practice site was not provided in the assignment instructions, this scraper is configured to target `http://quotes.toscrape.com`. This is the industry-standard sandbox environment specifically designed for safely testing web scraping pipelines. The bot implements polite crawling delays, valid User-Agent identification, and strict `robots.txt` adherence to demonstrate professional scraping etiquette.

## Features
* **Politeness Layer:** Strictly adheres to `robots.txt` rules using Python's `urllib.robotparser`.
* **Identification:** Sends a clear `User-Agent` header containing contact information so site administrators can identify the bot.
* **Rate Limiting:** Implements mandatory delays (2 seconds) between requests to prevent server strain.
* **Data Extraction & Cleaning:** Parses HTML using `BeautifulSoup4` to extract specific fields while stripping away unnecessary styling and scripts.
* **Structured Output:** Cleans and saves the extracted data into a structured `rag_corpus.json` file to serve as a high-quality corpus for next week's RAG implementation.

## Setup & Execution
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the scraper:

Bash
python scraper.py

3. The extracted dataset will be saved automatically to rag_corpus.json in the root directory.

Author

Ashutosh Nayak
ashutoshnayak0077@gmail.com