from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger("sj_scraper")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

start_url = "https://www.superjob.ru/vacancy/search/?catalogues%5B0%5D=603&catalogues%5B1%5D=627&catalogues%5B2%5D=628&catalogues%5B3%5D=629&catalogues%5B4%5D=36&catalogues%5B5%5D=37&catalogues%5B6%5D=38&catalogues%5B7%5D=503&catalogues%5B8%5D=40&catalogues%5B9%5D=42&catalogues%5B10%5D=546&catalogues%5B11%5D=604&catalogues%5B12%5D=650&catalogues%5B13%5D=45&catalogues%5B14%5D=46&catalogues%5B15%5D=47&catalogues%5B16%5D=48&catalogues%5B17%5D=51&catalogues%5B18%5D=52&catalogues%5B19%5D=53&catalogues%5B20%5D=54&catalogues%5B21%5D=56&catalogues%5B22%5D=49&catalogues%5B23%5D=50&catalogues%5B24%5D=614&geo%5Bt%5D%5B0%5D=4"
output_file = 'superjob_vacancy_links.txt'
page = 1
vacancy_links = set()

try:
    driver.get(start_url)
    logger.info(f"Открыта стартовая страница: {start_url}")
    with open(output_file, "a", encoding="utf-8") as f:
        while True:
            # Явно ждем появления карточек вакансий
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div._1rcGn.MdEH2")))
            logger.info(f"Страница {page}: карточки загружены, начинаю сбор ссылок")

            # Собираем все ссылки на вакансии внутри карточек по устойчивому href
            anchors = driver.find_elements(By.CSS_SELECTOR, 'div._1rcGn.MdEH2 a[href*="/vakansii/"]')

            for a in anchors:
                href = a.get_attribute("href")
                if not href:
                    continue
                # Нормализуем относительные ссылки, если встретятся
                if href.startswith("/"):
                    href = urljoin("https://www.superjob.ru", href)
                # Фильтр на всякий случай
                if "/vakansii/" in href:
                    # vacancy_links.add(href)
                    f.write(href + '\n')

            logger.info(f"Страница {page}: найдено {len(anchors)} ссылок")

            # Переход на следующую страницу
            try:
                next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.f-test-button-dalshe")))
                # Проверка на неактивную кнопку (если сайт так помечает)
                disabled = next_btn.get_attribute("aria-disabled") == "true" or "disabled" in (next_btn.get_attribute("class") or "")
                if disabled:
                    logger.info("Кнопка 'Далее' неактивна - достигнута последняя страница")
                    break
                # Клик с помощью JS на случай перекрытий
                driver.execute_script("arguments[0].click();", next_btn)
                logger.info("Клик по 'Далее', переход на следующую страницу")
                page += 1
                # Ждем подгрузку новой страницы/контента
                time.sleep(2)
            except Exception as e:
                logger.info(f"Кнопка 'Далее' не найдена/некликабельна")
                break

finally:
    driver.quit()

# Сохраняем в файл
with open(output_file, "r", encoding="utf-8") as f:
    vacancy_links = f.readlines()
    logger.info(f"Сохранено {len(vacancy_links)} ссылок в файл: {output_file}")