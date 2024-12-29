import json
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)


def write_to_json_file(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def _get_element_by_tag_and_string(driver, tag, keyword):
    elements = [el for el in driver.find_elements(By.TAG_NAME, tag) if keyword in el.text]
    if len(elements) > 0:
        return elements[0]
    else:
        return None


def parse_page_source(source):
    soup = BeautifulSoup(source, 'html.parser')
    divs = soup.find_all('div', class_='ULSxyf')
    links = []
    results = []
    for div in divs:
        # Find all <a> tags inside each <div> tag
        a_tags = div.find_all('a', href=True)  # Only get <a> tags with the href attribute

        for a_tag in a_tags:
            href = a_tag['href']  # Get the href value
            title_tag = a_tag.find('h3')
            if title_tag is None:
                continue
            title = title_tag.text
            if href.startswith(
                    'https://books.google.com/books?') and title.strip() != "" and title.strip() != "Preview" and href not in links:
                links.append(href)
                results.append({"title": title, "link": href})

    return results


def get_books_in_other_pages(url):
    driver.get(url)
    time.sleep(2)
    return parse_page_source(driver.page_source)


def search_in_google_books_tab(keyword):
    driver.get("https://www.google.com")

    try:
        # Find the search bar and input the keyword
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Click the 'Books' tab
        books_tab = _get_element_by_tag_and_string(driver, "a", "Books")
        books_tab.click()
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        page_links = ["https://www.google.com" + el['href'] for el in soup.find_all('a', attrs={'aria-label': True}) if
                      el.get('aria-label').startswith('Page')]

        results = parse_page_source(page_source)
        for link in page_links:
            results.extend(get_books_in_other_pages(link))

        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()


# Example usage
keyword = "Python programming books"
results = search_in_google_books_tab(keyword)
write_to_json_file("../test.json", results)
