from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

chrome_options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
web_driver_instance = webdriver.Chrome()

urls = []
words_to_check = ['sztucz', 'inteligencj', 'zastąp', 'zastap', ' ai ', ' si ', 'artificial', 'programist', 'potrzeba']

for i in range(1, 2):
    web_driver_instance.get('https://4programmers.net/Search?q=sztuczna+inteligencja&page=' + str(i))
    try:
        gdpr_button = web_driver_instance.find_element(By.ID, 'gdpr-none')
        gdpr_button.click()
    except:
        print('There is no gdpr button')

    webpage_source = web_driver_instance.page_source

    soup = BeautifulSoup(webpage_source, 'html.parser')

    ul_element = soup.find('ul', {'id': 'search-results'})
    a_tags = ul_element.find_all('a', href=True)

    base_url = "https://4programmers.net"

    for a_tag in a_tags:
        link = a_tag['href']
        full_url = link if link.startswith('http') else base_url + link
        urls.append(full_url)

unique_urls = list(dict.fromkeys(urls))
all_posts = []

for url in unique_urls:
    web_driver_instance.get(url)
    webpage_source = web_driver_instance.page_source
    soup = BeautifulSoup(webpage_source, 'html.parser')

    for blockquote in soup.find_all('blockquote'):
        blockquote.decompose()
    for footer in soup.find_all('footer'):
        footer.decompose()

    posts = soup.find_all('div', class_='post-content')

    # TODO: FIND ONLY POSTS THAT ARE IN words_to_check
    for post in posts:
        all_posts.append(post.text.strip())


output_file = 'posts.csv'

# Open the file in write mode
# Open a file in write mode
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for item in all_posts:
        writer.writerow([item])

print('Dlugosc listy to: ' + str(len(all_posts)))

# Read from the CSV file with UTF-8 encoding
counter = 0

with open('output.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        counter = counter + 1
        print(row)

print('Dlugosc listy to: ' + str(len(all_posts)))
print(counter)
