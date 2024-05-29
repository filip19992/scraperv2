from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


def setup_webdriver():
    """Setup and return a Selenium WebDriver instance with configured options."""
    chrome_options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=chrome_options)


def collect_urls(driver, pages=1):
    """Collect and return unique URLs from search results."""
    base_url = "https://4programmers.net"
    urls = []
    for i in range(1, pages + 1):
        driver.get(f'https://4programmers.net/Search?q=sztuczna+inteligencja&page={i}')
        try:
            gdpr_button = driver.find_element(By.ID, 'gdpr-none')
            gdpr_button.click()
        except:
            print('There is no GDPR button')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ul_element = soup.find('ul', {'id': 'search-results'})
        a_tags = ul_element.find_all('a', href=True)
        for a_tag in a_tags:
            link = a_tag['href']
            full_url = link if link.startswith('http') else base_url + link
            urls.append(full_url)
    return list(dict.fromkeys(urls))


def scrape_content(driver, url, keywords):
    """Scrape and return filtered content from a given URL based on specified keywords, removing duplicates."""
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for blockquote in soup.find_all('blockquote'):
        blockquote.decompose()
    for footer in soup.find_all('footer'):
        footer.decompose()
    posts = soup.find_all('div', class_='post-content')
    filtered_posts = set()  # Use a set to store unique posts
    for post in posts:
        post_text = post.text.strip()
        if any(word in post_text.lower() for word in keywords):
            filtered_posts.add(post_text + ';')  # Add the post to the set
    return list(filtered_posts)  # Convert the set back to a list for returning


def save_to_csv(data, filename):
    """Save a list of data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])


def read_and_print_csv(filename):
    """Read and print the content of a CSV file."""
    counter = 0
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            counter += 1
            print(row)
    return counter


def main():
    driver = setup_webdriver()
    keywords = ['sztucz', 'inteligencj', 'zastąp', 'zastap', ' ai ', ' si ', 'artificial', 'programist', 'potrzeba', 'wyprz', 'przysz', 'warto']

    print("Collecting URLs...")
    urls = collect_urls(driver, pages=2)

    print("Scraping content from URLs...")
    all_posts = []
    for url in urls:
        all_posts.extend(scrape_content(driver, url, keywords))

    driver.quit()

    output_file = 'output.csv'
    save_to_csv(all_posts, output_file)

    print("Reading and printing CSV content...")
    counter = read_and_print_csv(output_file)

    print(f'Total number of posts: {len(all_posts)}')
    print(f'Total number of rows in CSV: {counter}')


if __name__ == "__main__":
    main()
