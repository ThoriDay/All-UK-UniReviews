import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_review_data(url, university_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = []

    # Find all review boxes
    review_boxes = soup.find_all('div', class_='review-box')

    for review_box in review_boxes:
        # Extracting data from each review box
        review_content = review_box.find('div', class_='review-box__content')
        if review_content:
            rating = review_content.find('b').text  # Rating score
            username = review_content.find('em', class_='mini').find_all('span')[1].text  # Username
            review_text = review_content.find('p').text.strip()  # Review text

            # Extract the date
            date_info = review_content.find('em', class_='mini').find_all('span')
            if len(date_info) >= 3:
                date = date_info[2].next_sibling.strip()  # Get the text directly after the third span
            else:
                date = None  # Fallback if date extraction fails

            # Collecting ratings for categories
            ratings = {}
            ratings_div = review_content.find('div', class_='review-box__content__ratings')
            if ratings_div:
                category_boxes = ratings_div.find_all('div', class_='mb mt tw-pl-[34px]')
                for category in category_boxes:
                    category_name = category.find('b').text.strip()
                    category_rating = len(category.find('div', class_='stars').get('class')) - 1  # Count stars
                    ratings[category_name] = category_rating
            
            # Add the review information to the list, including university name
            reviews.append({
                'University': university_name,
                'Rating': rating,
                'Username': username,
                'Review': review_text,
                'Date': date,  # Add the date to the dictionary
                **ratings
            })

    return reviews

# List to hold all review data
all_reviews = []

# Read university URLs from a text file
with open('university_links.txt', 'r') as file:
    university_links = file.readlines()

# Loop through each university link
for uni_url in university_links:
    uni_url = uni_url.strip()  # Remove any whitespace or newline characters
    print(f"Scraping {uni_url}...")

    # Extract university name from the URL
    university_name = uni_url.split('/')[-1].replace('-',' ').title()  # Adjust to get a clean name

    # Scrape the first page to gather review data
    reviews = scrape_review_data(uni_url, university_name)
    all_reviews.extend(reviews)

    # Now, scrape the last page number from the pagination
    response = requests.get(uni_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the pagination section and extract the last page number
    pagination_links = soup.find_all('a', class_='link link--plain b text--bae c-sc-grey')
    if pagination_links:
        last_page_number = max(int(link.text.strip()) for link in pagination_links)  # Get the maximum page number from the links
    else:
        print("Could not find pagination links.")
        last_page_number = 1  # Default to 1 if not found

    # Loop through the remaining pages
    for page_number in range(2, last_page_number + 1):  # Start from page 2
        url = f"{uni_url}/reviews/{page_number}"  # Ensure pagination works correctly with the correct format
        print(f"Scraping {url}...")
        reviews = scrape_review_data(url, university_name)
        all_reviews.extend(reviews)

# Create a DataFrame from the collected data
df = pd.DataFrame(all_reviews)

# Save to CSV
df.to_csv('all_university_reviews.csv', index=False)
print("Data saved to all_university_reviews.csv.")
