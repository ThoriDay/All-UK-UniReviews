import requests
from bs4 import BeautifulSoup

def scrape_university_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links to universities
    university_links = []

    # Adjust the selector to target the correct <a> tags for universities
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Check if the link is to a university
        if href.startswith('https://www.studentcrowd.com/university-'):
            university_links.append(href)

    return university_links

# URL of the page containing university links
url = 'https://www.studentcrowd.com/page/university'  # Replace with the actual URL containing university links
university_links = scrape_university_links(url)

# Print all university links
for link in university_links:
    print(link)

# Optionally, save to a file
with open('university_links.txt', 'w') as f:
    for link in university_links:
        f.write(link + '\n')

print("University links saved to university_links.txt.")
