# UK Universities Reviews

## Overview
This project involves collecting and analyzing reviews of universities across the United Kingdom. Using **BeautifulSoup**, data was scraped from two websites to create a comprehensive dataset of university reviews. The final cleaned dataset, `final.csv`, is the result of combining and preprocessing the collected data.

---

## Features
- **Web Scraping**: Extract reviews data using Python and BeautifulSoup.
- **Data Cleaning**: Process and clean raw data into a structured format.
- **Output**: Unified dataset (`final.csv`) ready for analysis.

---

## How to Run the Project

### Prerequisites
Make sure you have the following installed:
- **Python** (>=3.7)
- Libraries: `BeautifulSoup`, `pandas`, `numpy`, `jupyter`

### Steps

1. **Run the Scraper**: Execute the `scraper.py` script to scrape raw data:
    ```bash
    python scraper.py
    ```

2. **Process Data**: Open and run the following Jupyter Notebook files sequentially:
    - `whatuni.ipynb`: Processes and saves data as `sample1.csv`.
    - `student_crowd.ipynb`: Processes and saves data as `sample2.csv`.

3. **Combine and Clean**: Run `analysis.ipynb` to combine and clean datasets:
    - **Inputs**: `sample1.csv`, `sample2.csv`
    - **Output**: `final.csv`

---

### File Structure

- **`scraper.py`**: Web scraping logic for extracting data.
- **`whatuni.ipynb`**: Cleans and processes data from the first website.
- **`student_crowd.ipynb`**: Cleans and processes data from the second website.
- **`analysis.ipynb`**: Combines and cleans the datasets into `final.csv`.
- **`final.csv`**: Final structured and cleaned dataset.

---

### Outputs

- **`sample1.csv`**: Dataset from the first website.
- **`sample2.csv`**: Dataset from the second website.
- **`final.csv`**: Merged and cleaned dataset containing all reviews.

---

### Future Work

- Scrape additional review websites to enhance data coverage.
- Perform sentiment analysis on the collected reviews.
- Create a dashboard for visualizing university ratings and reviews.

