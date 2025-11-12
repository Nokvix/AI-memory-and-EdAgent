import requests
import json
import time
import logging
import random
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class SuperJobParser:
    """Парсер вакансий с сайта SuperJob."""

    BASE_URL = "https://superjob.ru"
    HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }
    REQUEST_TIMEOUT = 10

    def __init__(self, output_file: str = 'superjob_vacancies.json'):
        """
        Инициализирует парсер.

        Args:
            output_file: Путь к файлу для сохранения результатов.
        """
        self.output_file = output_file
        self.vacancies = []

    def fetch_vacancy_links_from_file(
            self,
            filename: str
    ) -> List[str]:
        """
        Читает ссылки на вакансии из текстового файла.

        Args:
            filename: Путь к файлу со ссылками на вакансии.

        Returns:
            Список URL вакансий.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                links = [line.strip() for line in f if line.strip()]
            logger.info(
                f"Загружено {len(links)} ссылок на вакансии из {filename}"
            )
            return links
        except FileNotFoundError:
            logger.error(f"Файл {filename} не найден")
            return []

    def _get_vacancy_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Получает и парсит страницу вакансии.

        Args:
            url: URL вакансии.

        Returns:
            BeautifulSoup объект или None если запрос неудачен.
        """
        try:
            response = requests.get(
                url,
                headers=self.HEADERS,
                timeout=self.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response.encoding = 'utf-8'
            return BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            logger.warning(f"Ошибка загрузки {url}: {e}")
            return None

    def _extract_position(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Извлекает должность из тега h1.

        Args:
            soup: BeautifulSoup объект.

        Returns:
            Название должности или None.
        """
        try:
            position_elem = soup.find('h1')
            if position_elem:
                position = position_elem.get_text(strip=True)
                logger.debug(f"Должность: {position}")
                return position
        except Exception as e:
            logger.debug(f"Ошибка извлечения должности: {e}")
        return None

    def _extract_company_name(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Извлекает название компании.

        Args:
            soup: BeautifulSoup объект.

        Returns:
            Название компании или None.
        """
        try:
            company_link = soup.select_one('a._2KL7K._3xRR0.rNYlz')

            if company_link:
                company_name = company_link.get_text(strip=True)
                logger.debug(f"Компания: {company_name}")
                return company_name
        except Exception as e:
            logger.debug(f"Ошибка извлечения компании: {e}")
        return None

    def _extract_company_url(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Извлекает URL компании.

        Args:
            soup: BeautifulSoup объект.

        Returns:
            URL компании или None.
        """
        try:
            company_link = soup.select_one('a._2KL7K._3xRR0.rNYlz')
            if company_link and company_link.has_attr('href'):
                href = company_link['href']
                company_url = urljoin(self.BASE_URL, href)
                logger.debug(f"URL компании: {company_url}")
                return company_url
        except Exception as e:
            logger.debug(f"Ошибка извлечения URL компании: {e}")
        return None

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Извлекает описание вакансии из div с классом mrLsm.

        Args:
            soup: BeautifulSoup объект.

        Returns:
            Описание вакансии или None.
        """
        try:
            description_elem = soup.find('span', class_='mrLsm')
            if description_elem:
                description = ""
                for elem in description_elem.find_all(
                    ['p', 'li', 'ul']
                ):
                    if elem.name == 'p':
                        description += elem.get_text(strip=True) + " "
                    elif elem.name == 'li':
                        description += (
                            "• " + elem.get_text(strip=True) + " "
                        )

                description = description.strip()
                logger.debug(
                    f"Описание получено, длина: {len(description)}"
                )
                return description
        except Exception as e:
            logger.debug(f"Ошибка извлечения описания: {e}")
        return None

    def _extract_main_skills(self, soup: BeautifulSoup) -> List[str]:
        """
        Извлекает профессиональные навыки.

        Args:
            soup: BeautifulSoup объект.

        Returns:
            Список навыков.
        """
        try:
            skills = []
            skill_ul = soup.find('ul', class_='_8jaXR l1uNA _2vT41 _1B3_w rQxxF')
            skill_lis = skill_ul.find_all('li', class_='EgYWq')

            for skill_li in skill_lis:
                skill_span = skill_li.find('span', class_='_3G1g8')
                if skill_span:
                    skill_text = skill_span.get_text(strip=True)
                    if skill_text:
                        skills.append(skill_text)

            seen = set()
            skills = [
                s for s in skills
                if not (s in seen or seen.add(s))
            ]

            logger.debug(f"Навыки: {', '.join(skills)}")
            return skills
        except Exception as e:
            logger.debug(f"Ошибка извлечения навыков: {e}")
        return []

    def parse_vacancy(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Парсит одну вакансию и извлекает все требуемые данные.

        Args:
            url: URL вакансии.

        Returns:
            Словарь с данными вакансии или None при ошибке.
        """
        logger.info(f"Парсинг вакансии: {url}")

        soup = self._get_vacancy_page(url)
        if not soup:
            return None

        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())

        vacancy_data = {
            'position': self._extract_position(soup),
            'company_name': self._extract_company_name(soup),
            'company_url': self._extract_company_url(soup),
            'description': self._extract_description(soup),
            'main_skills': self._extract_main_skills(soup),
            'vacancy_url': url
        }

        logger.info("Вакансия успешно распарсена")
        return vacancy_data

    def parse_vacancies_from_file(
            self,
            vacancy_file: str = 'vacancy_links.txt',
            delay: float = 1.0
    ) -> None:
        """
        Парсит все вакансии из файла со ссылками.

        Args:
            vacancy_file: Путь к файлу со ссылками на вакансии.
            delay: Задержка между запросами в секундах.
        """
        links = self.fetch_vacancy_links_from_file(vacancy_file)
        if not links:
            logger.error("Нет ссылок для обработки")
            return

        total_links = len(links)

        for idx, link in enumerate(links, 1):
            logger.info(f"Обработка {idx}/{total_links}")
            vacancy_data = self.parse_vacancy(link)
            if vacancy_data:
                self.vacancies.append(vacancy_data)
            time.sleep(delay)

        self.save_to_json()

    def parse_vacancy_direct(self, url: str) -> None:
        """
        Парсит одну вакансию напрямую по URL.

        Args:
            url: URL вакансии.
        """
        vacancy_data = self.parse_vacancy(url)
        if vacancy_data:
            self.vacancies.append(vacancy_data)
            self.save_to_json()

    def save_to_json(self) -> None:
        """Сохраняет собранные вакансии в JSON файл."""
        if not self.vacancies:
            logger.warning("Нет данных для сохранения")
            return

        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(
                    self.vacancies,
                    f,
                    ensure_ascii=False,
                    indent=4
                )
            logger.info(
                f"Сохранено {len(self.vacancies)} вакансий в "
                f"{self.output_file}"
            )
        except IOError as e:
            logger.error(f"Ошибка при сохранении JSON: {e}")

    def get_vacancies(self) -> List[Dict[str, Any]]:
        """
        Возвращает список распарсенных вакансий.

        Returns:
            Список словарей с данными вакансий.
        """
        return self.vacancies


def main():
    """Основная функция."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    parser = SuperJobParser(output_file='superjob_vacancies.json')
    # parser.parse_vacancy_direct('https://zvenigorod.superjob.ru/vakansii/glavnyj-specialist-otdela-avtomatizacii-50517180.html')
    parser.parse_vacancies_from_file(
        vacancy_file='superjob_vacancy_links.txt',
        delay=random.uniform(2, 5)
    )


if __name__ == "__main__":
    main()
