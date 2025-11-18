from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import csv
import json
from urllib.parse import quote  # для безопасного формирования URL


class LinkedInLinksParser:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

    def init_driver(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def scroll_page(self, max_scrolls=10):
        """Прокручивает страницу для загрузки вакансий (infinite scroll)"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0

        while scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            scrolls += 1

    def parse_job_links(self, keywords, location, max_pages=3):
        """Собирает ссылки на вакансии LinkedIn"""
        self.init_driver()
        job_links = []

        try:
            for page in range(max_pages):
                start = page * 25
                url = (
                    "https://www.linkedin.com/jobs/search/"
                    f"?keywords={quote(keywords)}"
                    f"&location={quote(location)}"
                    f"&start={start}"
                )

                print(f"Парсинг страницы {page + 1}...")
                self.driver.get(url)
                time.sleep(3)

                self.scroll_page()

                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.base-card")

                for card in job_cards:
                    try:
                        link_element = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")
                        vacancy_url = link_element.get_attribute('href')

                        if vacancy_url and '?' in vacancy_url:
                            vacancy_url = vacancy_url.split('?', 1)[0]  # ВАЖНО: берём только строку до '?'

                        if not vacancy_url:
                            continue

                        if vacancy_url not in job_links:
                            job_links.append(vacancy_url)

                    except Exception:
                        continue

                print(f"Найдено ссылок: {len(job_links)}")

        except Exception as e:
            print(f"Ошибка при парсинге ссылок: {e}")
        finally:
            self.driver.quit()

        return job_links

    def save_to_txt(self, job_links, filename="vacansies-links.txt"):
        """Сохраняет ссылки в обычный txt-файл, по одной ссылке в строке"""
        with open(filename, 'w', encoding='utf-8') as file:
            for link in job_links:
                file.write(str(link).strip() + "\n")
        print(f"Сохранено {len(job_links)} ссылок в {filename}")


if __name__ == "__main__":
    parser = LinkedInLinksParser(headless=True)

    keywords = "Python Developer"
    location = "United States"
    max_pages = 5

    links = parser.parse_job_links(keywords, location, max_pages)
    parser.save_to_txt(links)
