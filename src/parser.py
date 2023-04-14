import asyncio
from loguru import logger
from sqlalchemy.dialects.postgresql import insert
from utils import request_metro_news, get_info_news
from database import async_session_maker
from models import news as news_model


async def main() -> None:
    """ Точка старта парсера. Парсит новости каждые 10 мин с последних 5 страниц сайта и записывает данные в базу """
    while 1:
        logger.info("Start parse News MosMetro by first 5 pages!")
        tasks = [asyncio.create_task(request_metro_news(number_page=number_page)) for number_page in range(1, 6)]
        html_pages = await asyncio.gather(*tasks)
        for html in html_pages:
            news = get_info_news(html=html)
            if not news:
                logger.warning(f"No found news by Page. Continue...")
                continue
            async with async_session_maker() as session:
                await session.execute(insert(news_model).on_conflict_do_nothing(), news)
                await session.commit()
            logger.info(f"Successfully written to the database {len(news)} news.")
        logger.info("Sleep parser 10 minutes.")
        await asyncio.sleep(600)


if __name__ == '__main__':
    asyncio.run(main())
