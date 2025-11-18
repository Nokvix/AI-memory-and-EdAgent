from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import json


class LinkedInJobsParser:
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

    def parse_job_detail(self, url):
        """Парсит детальную информацию о вакансии"""
        try:
            self.driver.get(url)
            time.sleep(3)

            job_data = {
                'position': None,
                'company_name': None,
                'company_url': None,
                'description': None,
                'location': None,
                'employment_type': None,
                'seniority_level': None,
                'main_skills': [],
                'vacancy_url': url
            }
            try:
                position = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "h1.top-card-layout__title"
                ).text
                job_data['position'] = position.strip()

            except Exception:
                pass

            try:
                company_element = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "a.topcard__org-name-link"
                )
                job_data['company_name'] = company_element.text.strip()
                job_data['company_url'] = company_element.get_attribute('href')
            except Exception:
                try:
                    company_name = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "span.topcard__flavor"
                    ).text
                    job_data['company_name'] = company_name.strip()
                except Exception:
                    pass

            try:
                location = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "span.topcard__flavor--bullet"
                ).text
                job_data['location'] = location.strip()
            except Exception:
                pass

            try:
                try:
                    show_more_btn = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "button.show-more-less-html__button"
                    )
                    show_more_btn.click()
                    time.sleep(1)
                except Exception:
                    pass

                description = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "div.show-more-less-html__markup"
                ).text
                job_data['description'] = description.strip()
            except Exception:
                pass

            try:
                criteria_items = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "li.description__job-criteria-item"
                )
                for item in criteria_items:
                    try:
                        header = item.find_element(
                            By.CSS_SELECTOR,
                            "h3"
                        ).text.strip()
                        value = item.find_element(
                            By.CSS_SELECTOR,
                            "span"
                        ).text.strip()

                        if "Employment type" in header:
                            job_data['employment_type'] = value
                        elif "Seniority level" in header:
                            job_data['seniority_level'] = value
                    except Exception:
                        continue
            except Exception:
                pass

            if job_data['description']:
                common_skills = [
                    'Python', 'Java', 'JavaScript', 'SQL', 'AWS', 'Docker',
                    'Kubernetes', 'React', 'Node.js', 'Git', 'CI/CD', 'Agile'
                ]
                found_skills = []
                description_lower = job_data['description'].lower()

                for skill in common_skills:
                    if skill.lower() in description_lower:
                        found_skills.append(skill)

                job_data['main_skills'] = found_skills

            return job_data

        except Exception as e:
            print(f"Ошибка при парсинге вакансии {url}: {e}")
            return None

    def parse_jobs_from_txt(self, input_file="vacansies-links.csv"):
        """Читает ссылки из CSV и парсит каждую вакансию"""
        self.init_driver()
        jobs_data = []

        try:
            with open("vacansies-LINKS.txt", "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]

            print(f"Найдено {len(urls)} вакансий для парсинга")

            for idx, url in enumerate(urls, 1):
                print(f"Парсинг вакансии {idx}/{len(urls)}...")
                job_data = self.parse_job_detail(url)

                if job_data:
                    jobs_data.append(job_data)

                time.sleep(2)

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
        finally:
            self.driver.quit()

        return jobs_data

    def save_to_json(self, jobs_data, filename="vacansies.json"):
        """Сохраняет данные вакансий в JSON"""
        if not jobs_data:
            print("Нет данных для сохранения")
            return

        # json.dump умеет сохранять list[dict] напрямую
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs_data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено {len(jobs_data)} вакансий в {filename}")


if __name__ == "__main__":
    parser = LinkedInJobsParser(headless=True)
    jobs = parser.parse_jobs_from_txt("vacansies-links.csv")
    parser.save_to_json(jobs)
