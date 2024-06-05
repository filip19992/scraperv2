from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


def setup_webdriver():
    chrome_options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    return webdriver.Chrome(options=chrome_options)


def collect_urls(driver, pages=1):
    base_url = "https://4programmers.net"
    urls = []
    urls_to_search = ['https://4programmers.net/Search?q=sztuczna+inteligencja&page=',
                      'https://4programmers.net/Search?q=AI&page=',
                      'https://4programmers.net/Search?q=artificial+intelligence&page=',
                      'https://4programmers.net/Search?q=devin&page=',
                      'https://4programmers.net/Search?q=chat+gpt&page=',
                      'https://4programmers.net/Search?q=copilot&page=']
    for url in urls_to_search:
        for i in range(1, pages + 1):
            driver.get(f'{url}{i}')
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
    filtered_posts = []
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for blockquote in soup.find_all('blockquote'):
            blockquote.decompose()
        for footer in soup.find_all('footer'):
            footer.decompose()
        posts = soup.find_all('div', class_='post-content')
        for post in posts:
            post_text = post.text.strip()
            if any(word in post_text.lower() for word in keywords):
                filtered_posts.append(post_text + ';')
    except:
        print('Unable to scrap this page')

    return filtered_posts


def remove_duplicates(input_list):
    # Use a set to track seen elements
    seen = set()
    unique_list = []

    for item in input_list:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)

    return unique_list


def save_to_csv(data, filename):
    """Save a list of data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item.replace('\n', ' ')])


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
    output_file = 'output-4.csv'

    driver = setup_webdriver()
    keywords = ['zastąp', 'zastap', 'zastąpić', 'zastapic', 'sztuczna inteligencja nie potrafi', 'ai nie potrafi',
                'programiści są bezpieczni', 'wyprze', 'wyparci', 'sa bezpieczni', 'ai zastapi', 'ai nie zastapi',
                'zastapi', 'nie sa bezpieczni', 'narazie sztuczna inteligencja', 'narazie ai',
                'sztuczna inteligencja jest dobra', 'sztuczna inteligencja jest beznadziejna', 'sztuczna inteligencja jest slaba',
                'sztuczna inteligencja jest przereklamowana', 'sztuczna inteligencja nie umie', 'sztuczna inteligencja nie rozumie',
                'sztuczna inteligencja jest dobra w']

    print("Collecting URLs...")
    urls = collect_urls(driver, pages=150)

    print("Scraping content from URLs...")
    all_posts = []
    for url in urls:
        all_posts.extend(scrape_content(driver, url, keywords))

    posts_without_duplicates = remove_duplicates(all_posts)
    driver.quit()

    save_to_csv(posts_without_duplicates, output_file)

    print("Reading and printing CSV content...")
    counter = read_and_print_csv(output_file)

    print(f'Total number of posts: {len(all_posts)}')
    print(f'Total number of rows in CSV: {counter}')


if __name__ == "__main__":
    main()
