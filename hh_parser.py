from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

def parse_hh_vacancies(url, output_file='vacancy_links.txt'):
    """
    Parse vacancy links from hh.ru and save them to a text file.

    Args:
        url (str): The hh.ru search URL
        output_file (str): Output filename for saving links
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    try:
        print(f"Opening URL: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        vacancy_links = set()
        page_num = 0

        with open(output_file, 'a', encoding='utf-8') as f:
            while True:
                page_num += 1
                print(f"\nParsing page {page_num}...")

                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')))
                    time.sleep(2)  # Additional wait for dynamic content
                except TimeoutException:
                    print("Timeout waiting for vacancy cards. Breaking...")
                    break

                vacancy_cards = driver.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy"]')

                if not vacancy_cards:
                    print("No vacancy cards found on this page.")
                    break

                print(f"Found {len(vacancy_cards)} vacancy cards on page {page_num}")

                for card in vacancy_cards:
                    try:
                        link_element = card.find_element(By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]')
                        vacancy_url = link_element.get_attribute('href')

                        if vacancy_url:
                            f.write(vacancy_url + '\n')

                    except NoSuchElementException:
                        continue

                print(f"Total unique links collected so far: {len(vacancy_links)}")

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, '[data-qa="pager-next"]')

                    if next_button and next_button.is_enabled():
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        time.sleep(1)

                        next_button.click()
                        time.sleep(3)
                    else:
                        print("Next button is disabled or not found. Reached last page.")
                        break

                except NoSuchElementException:
                    print("No more pages available.")
                    break

        with open(output_file, 'r', encoding='utf-8') as f:
            vacancy_links = f.readlines()
            print(f"\n{'='*60}")
            print(f"Successfully saved {len(vacancy_links)} unique vacancy links to '{output_file}'")
            print(f"{'='*60}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    TARGET_URL = "https://ekaterinburg.hh.ru/search/vacancy?area=3&professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126&withTopFilterCatalog=true&hhtmFrom=main"

    OUTPUT_FILE = "vacancy_links.txt"

    parse_hh_vacancies(TARGET_URL, OUTPUT_FILE)
