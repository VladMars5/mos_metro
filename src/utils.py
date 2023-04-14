import aiohttp
import aiohttp.client_exceptions
from loguru import logger
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime


async def request_metro_news(number_page: int) -> str:
    """ Функция для выполнения запросов на сайт для получения html страницы с новостями.
        number_page: номер страницы новостей """
    if number_page < 1:
        return ''
    elif number_page == 1:
        number_page = ''
    async with aiohttp.ClientSession() as session:
        logger.info(f'Request News MosMetro by number page ---> {number_page}')
        try:
            async with session.get(f'https://mosday.ru/news/tags.php?metro_{number_page}', timeout=10) as response:
                html = await response.text()
                return html
        except aiohttp.client_exceptions.ClientConnectorError as err:
            logger.error(f"Fail Connection request: {err}")
        except asyncio.exceptions.TimeoutError as err:
            logger.error(f"Fail Timeout request: {err}")
        except Exception as ex:
            logger.error(f"Exception Error: {ex}")
    return ''


def get_info_news(html: str) -> list:
    """ Функция для парсинга информации по новостям из html документа """
    result_news = []
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table', attrs={"width": "95%", "cellpadding": "0", "cellspacing": "10",
                                           "border": "0", "style": "font-family:Arial;font-size:15px"})
    for table in tables:
        news = table.find_all('tr')
        for new in news:
            try:
                title = new.find_all('td')[-1].find('font').find('font').find('b').text
                date = new.find_all('td')[-1].find('b').text
            except Exception as ex:
                logger.error(f'No found title or date article. Error: {ex}. Continue news ...')
                continue
            try:
                link_picture = f"https://mosday.ru/news/{new.find('img')['src']}"
            except Exception as ex:
                logger.warning(f'No found link picture. Error: {ex}')
                link_picture = ''
            logger.info(f"Parse News Data -> Title: {title} | Date: {date} | LinkPicture: {link_picture}")
            result_news.append({"title": title, "date":  datetime.strptime(date, '%d.%m.%Y').date(),
                                "url_picture": link_picture})
    return result_news
