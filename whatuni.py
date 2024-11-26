import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_review_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = []

    # Find all review rows
    review_rows = soup.find_all('div', class_='rlst_row')

    for review_row in review_rows:
        # Extract the university name
        university_name_tag = review_row.find('h2')
        university_name = university_name_tag.a['data-review-collagename'] if university_name_tag and university_name_tag.a else None

        # Extract the course name
        course_name_tag = review_row.find('h3')
        course_name = course_name_tag.a.text.strip() if course_name_tag and course_name_tag.a else None

        # Initialize university rating variable
        university_rating = None

        # Locate the rating within the review row
        rating_div = review_row.find('div', class_='rate_new')
        if rating_div:
            # Look for the specific span that contains the university rating
            rating_value = rating_div.find('span', string=lambda text: text and text.strip().startswith('('))
            if rating_value:
                # Extract the numeric rating from the text
                university_rating = rating_value.text.strip('()')  # Remove parentheses

        # Extract the review text
        overall_comment = review_row.find('p', id=lambda x: x and x.startswith('overallCommentId'))
        review_text = overall_comment.text.strip() if overall_comment else None

        # Extract the review date
        review_date = review_row.find('div', class_='reviewed-year')
        review_date = review_date.text.strip().replace('Reviewed: ', '') if review_date else None

        # Append extracted data to reviews list
        reviews.append({
            'University': university_name,
            'Course Name': course_name,
            'University Rating': university_rating,
            'Review': review_text,
            'Date': review_date
        })

    return reviews

# Base URL for the first page
base_url = 'https://www.whatuni.com/university-course-reviews/'

# Get the total number of pages dynamically
def get_total_pages(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the pagination element
    pagination = soup.find('ul', class_='pagn')

    if pagination:
        # Find the last pagination link and extract the page number
        last_page_link = pagination.find_all('li')[-2].find('a')  # Second to last <li> contains the last page number
        if last_page_link and last_page_link['href']:
            return int(last_page_link['href'].split('pageno=')[-1])  # Extract page number from the URL
    
    return 1  # Default to 1 if no pagination found

# Get total pages
total_pages = get_total_pages(base_url)
print(f"Total pages found: {total_pages}")

# Initialize a list to hold all reviews
all_reviews = []

# Scrape each page
for page in range(1, total_pages + 1):
    # Construct the URL for each page
    if page == 1:
        url = base_url  # First page does not have a page number
    else:
        url = f'https://www.whatuni.com/university-course-reviews?pageno={page}'

    print(f"Scraping {url}...")
    reviews = scrape_review_data(url)
    all_reviews.extend(reviews)  # Add reviews from this page to the overall list

# Create a DataFrame from the collected data
df = pd.DataFrame(all_reviews)

# Save to CSV
df.to_csv('whatuni_reviews.csv', index=False)
print("Data saved to whatuni_reviews.csv.")
