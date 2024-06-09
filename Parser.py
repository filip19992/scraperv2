from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re


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


def scrape_content(driver, url, regex_patterns):
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
            if any(re.search(pattern, post_text.lower()) for pattern in regex_patterns):
                filtered_posts.append(post_text + ';')
    except:
        print('Unable to scrap this page')

    return filtered_posts


def remove_duplicates(input_list):
    seen = set()
    unique_list = []
    for item in input_list:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item.replace('\n', ' ')])


def read_and_print_csv(filename):
    counter = 0
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            counter += 1
            print(row)
    return counter


def get_keywords():
    return [
        r'\bzast[ąa]p[ićic]\b',
        r'\bsztuczna inteligencja nie potrafi\b',
        r'\bai nie potrafi\b',
        r'\bprogrami[śs]ci s[ąa] bezpieczni\b',
        r'\bwyprze\b',
        r'\bwyparci\b',
        r'\bs[ąa] bezpieczni\b',
        r'\bai zast[ąa]pi\b',
        r'\bai nie zast[ąa]pi\b',
        r'\bzast[ąa]pi\b',
        r'\bnie s[ąa] bezpieczni\b',
        r'\bnarazie sztuczna inteligencja\b',
        r'\bnarazie ai\b',
        r'\b(sztuczna inteligencja|AI) jest dobra\b',
        r'\b(sztuczna inteligencja|AI) beznadziejna\b',
        r'\b(sztuczna inteligencja|AI) s[łl]aba\b',
        r'\b(sztuczna inteligencja|AI) przereklamowana\b',
        r'\b(sztuczna inteligencja|AI)umie\b',
        r'\b(sztuczna inteligencja|AI)rozumie\b',
        r'\b(sztuczna inteligencja|AI) dobra w\b',
        r'\bzastosowanie sztucznej inteligencji\b',
        r'\bzastosowanie ai\b',
        r'\bpor[óo]wnanie sztucznej inteligencji\b',
        r'\bpor[óo]wnanie ai\b',
        r'\bprzysz[łl]o[śs][ćc] sztucznej inteligencji\b',
        r'\bprzysz[łl]o[śs][ćc] ai\b',
        r'\bsztuczna inteligencja to przyszłość\b',
        r'\bsztuczna inteligencja w medycynie\b',
        r'\bsztuczna inteligencja w finansach\b',
        r'\bsztuczna inteligencja w edukacji\b',
        r'\bsztuczna inteligencja w przemy[śs]le\b',
        r'\bsztuczna inteligencja w rolnictwie\b',
        r'\bsztuczna inteligencja w marketingu\b',
        r'\bsztuczna inteligencja w sztuce\b',
        r'\bsztuczna inteligencja w rozrywce\b',
        r'\bsztuczna inteligencja w pracy\b',
        r'\bsztuczna inteligencja w codziennym życiu\b',
        r'\bsztuczna inteligencja zmienia świat\b',
        r'\brozpoznawanie obrazu\b',
        r'\bprzetwarzanie języka naturalnego\b',
        r'\buczenie maszynowe\b',
        r'\bgłębokie uczenie\b',
        r'\bsieci neuronowe\b',
        r'\bmodele językowe\b',
        r'\binteligentne systemy\b',
        r'\bsztuczna inteligencja a etyka\b',
        r'\bsztuczna inteligencja a bezpieczeństwo\b',
        r'\bsztuczna inteligencja a zarządzanie\b',
        r'\bsztuczna inteligencja a polityka\b',
        r'\bsztuczna inteligencja a społeczeństwo\b',
        r'\bprzyszłość AI\b',
        r'\brozwój sztucznej inteligencji\b',
        r'\bwyzwania sztucznej inteligencji\b',
        r'\bzagrożenia sztucznej inteligencji\b',
        r'\bmożliwości sztucznej inteligencji\b',
        r'\bkorzyści ze sztucznej inteligencji\b',
        r'\bnauczanie maszynowe\b',
        r'\bwspomaganie decyzji\b',
        r'\bautomatyzacja zadań\b',
        r'\brozwój AI\b',
        r'\binnowacje w AI\b',
        r'\btechnologie AI\b',
        r'\bprzemysł 4.0\b',
        r'\b(sztuczna inteligencja|AI) zast[ąa]pi (pracownik[óo]w|nas|ludzi)\b',
        r'\b(sztuczna inteligencja|AI) wyprze (grafik[óo]w|programist[óo]w|pracownik[óo]w|ludzi)\b',
        r'\bczy (sztuczna inteligencja|AI) zast[ąa]pi\b',
        r'\bczy (sztuczna inteligencja|AI) wyprze\b',
        r'\bw przysz[łl]o[śs]ci (sztuczna inteligencja|AI) zast[ąa]pi\b',
        r'\bw przysz[łl]o[śs]ci (sztuczna inteligencja|AI) wyprze\b',
        r'\bprzez (sztuczn[ąa] inteligencj[ęe]|AI) strac[ęe|imy|i] prac[ęe|y]\b',
        r'\b(sztuczna inteligencja|AI) odbierze nam prac[ęe|y]\b',
        r'\b(sztuczna inteligencja|AI) odbiera prac[ęe|y]\b',
        r'\bzawody zagrożone przez (sztuczn[ąa] inteligencj[ęe]|AI)\b',
        r'\bpraca zagrożona przez (sztuczn[ąa] inteligencj[ęe]|AI)\b',
        r'\bboję si[ęe], że (sztuczna inteligencja|AI) zast[ąa]pi\b',
        r'\bobawiam si[ęe], że (sztuczna inteligencja|AI) wyprze\b',
        r'\bprzysz[łl]o[śs][ćc] pracy z (sztuczn[ąa] inteligencj[ąa]|AI)\b',
        r'\b(sztuczna inteligencja|AI) zmieni rynek pracy\b',
        r'\bczy moje stanowisko zast[ąa]pi (sztuczna inteligencja|AI)\b',
        r'\bczy moje stanowisko wyprze (sztuczna inteligencja|AI)\b',
        r'\bczy (sztuczna inteligencja|AI) przejmie moją prac[ęe]\b',
        r'\b(sztuczna inteligencja|AI) w pracy\b',
        r'\bzast[ąa]pi mnie (sztuczna inteligencja|AI)\b',
        r'\b(sztuczna inteligencja|AI) przejmie\b',
        r'\b(sztuczna inteligencja|AI) zrobi to lepiej ni[żz] ludzie\b',
        r'\bzast[ąa]pi pracownik[óo]w (sztuczna inteligencja|AI)\b',
        r'\b(sztuczna inteligencja|AI) zabiera prac[ęe|y]\b',
        r'\b(sztuczna inteligencja|AI) zast[ąa]pi ludzi\b',
        r'\bpraca dla (sztucznej inteligencji|AI)\b',
        r'\bprzysz[łl]o[śs][ćc] rynku pracy a (sztuczna inteligencja|AI)\b',
        r'\bzawody zagrożone przez (sztuczna inteligencja|AI)\b',
        r'\b(zast[ąa]pi|wyprze) ludzi (sztuczna inteligencja|AI)\b',
        r'\b(sztuczna inteligencja|AI) pomo[żz]e\b',
        r'\b(sztuczna inteligencja|AI) usprawni\b',
        r'\b(sztuczna inteligencja|AI) ułatwi\b',
        r'\b(sztuczna inteligencja|AI) poprawi\b',
        r'\b(sztuczna inteligencja|AI) zwiekszy wydajno[śs][ćc]\b',
        r'\b(sztuczna inteligencja|AI) zwiększy efektywno[śs][ćc]\b',
        r'\b(sztuczna inteligencja|AI) zrewolucjonizuje\b',
        r'\b(sztuczna inteligencja|AI) stworzy nowe mo[żz]liwo[śs]ci\b',
        r'\b(sztuczna inteligencja|AI) mo[żz]e zast[ąa]pi[ćc] powtarzalne prace\b',
        r'\b(sztuczna inteligencja|AI) odcią[żz]y ludzi od monotonnych zada[ńn]\b',
        r'\b(sztuczna inteligencja|AI) pomo[żz]e w rozwoju\b',
        r'\b(sztuczna inteligencja|AI) otworzy nowe rynki\b',
        r'\b(sztuczna inteligencja|AI) usprawni prac[ęe]\b',
        r'\b(sztuczna inteligencja|AI) przyspieszy procesy\b',
        r'\b(sztuczna inteligencja|AI) podniesie jako[śs][ćc] usług\b',
        r'\b(sztuczna inteligencja|AI) pomo[żz]e w kreatywnych zadaniach\b',
        r'\b(sztuczna inteligencja|AI) sprawi, [żz]e praca b[ęe]dzie łatwiejsza\b',
        r'\b(sztuczna inteligencja|AI) zautomatyzuje nudne zadania\b',
        r'\b(sztuczna inteligencja|AI) usprawni zarz[ąa]dzanie\b',
        r'\b(sztuczna inteligencja|AI) podniesie efektywno[śs][ćc] firmy\b',
        r'\b(sztuczna inteligencja|AI) zwi[ęe]kszy innowacyjno[śs][ćc]\b',
        r'\b(sztuczna inteligencja|AI) przyniesie korzy[śs]ci\b',
        r'\b(sztuczna inteligencja|AI) poprawi jako[śs][ćc] pracy\b',
        r'\b(sztuczna inteligencja|AI) ułatwi codzienne zadania\b',
        r'\b(sztuczna inteligencja|AI) pomo[żz]e w skomplikowanych procesach\b',
        r'\b(sztuczna inteligencja|AI) zwi[ęe]kszy produktywno[śs][ćc]\b',
        r'\b(sztuczna inteligencja|AI) zmniejszy koszty\b',
        r'\b(sztuczna inteligencja|AI) pomo[żz]e ludziom\b',
        r'\b(sztuczna inteligencja|AI) wspomo[żz]e\b',
        r'\b(sztuczna inteligencja|AI) da nowe mo[żz]liwo[śs]ci zawodowe\b',
        r'\b(sztuczna inteligencja|AI) mo[żz]e pom[óo]c w nauce\b',
        r'\b(sztuczna inteligencja|AI) otworzy nowe sektory\b',
        r'\b(sztuczna inteligencja|AI) zwi[ęe]kszy nasze mo[żz]liwo[śs]ci\b',
        r'\b(sztuczna inteligencja|AI) ułatwi [żz]ycie\b',
        r'\b(sztuczna inteligencja|AI) usprawni dzia[łl]anie\b',
        r'\b(sztuczna inteligencja|AI) poprawi komunikacj[ęe]\b',
        r'\b(sztuczna inteligencja|AI) pomo[żz]e w podejmowaniu decyzji\b']


def main():
    output_file = 'output-5.csv'

    driver = setup_webdriver()

    regex_patterns = get_keywords()

    print("Collecting URLs...")
    urls = collect_urls(driver, pages=150)

    print("Scraping content from URLs...")
    all_posts = []
    for url in urls:
        all_posts.extend(scrape_content(driver, url, regex_patterns))

    posts_without_duplicates = remove_duplicates(all_posts)
    driver.quit()

    save_to_csv(posts_without_duplicates, output_file)

    print("Reading and printing CSV content...")
    counter = read_and_print_csv(output_file)

    print(f'Total number of posts: {len(all_posts)}')
    print(f'Total number of rows in CSV: {counter}')


if __name__ == "__main__":
    main()
