from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import news as news_model
from database import get_async_session
from datetime import date, timedelta
from schemas import NewsInfo, NewsPeriod
from typing import List

app = FastAPI(
    title="API MosMetro"
)


@app.get("/")
async def start_page() -> str:
    return "Welcome to Test API News MosMetro. Go to /docs and make request !!!"


@app.get("/metro/news")
async def get_last_news(day: int = 0, session: AsyncSession = Depends(get_async_session)) -> List[NewsInfo]:
    """ Запрос на получение новостей за прошедшие n дней. Максимальное кол-во прошедших дней 14 """
    if day < 0:  # валидация на неотрицательное число
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of days elapsed cannot be negative",
        )
    elif day > 14:  # дополнительно ограничение (максимум выдавать новости за последние 14 дней)
        day = 14
    current_date = date.today()
    before_date_news = current_date - timedelta(days=day)
    query = select(news_model.c.title, news_model.c.date, news_model.c.url_picture).filter(news_model.c.date.between(
        before_date_news, current_date))
    news = await session.execute(query)
    return [NewsInfo(**new._mapping) for new in news]


@app.post("/metro/news_period")
async def get_profile_id_by_username(period: NewsPeriod, session: AsyncSession = Depends(get_async_session)) \
        -> List[NewsInfo]:
    """ Дополнительный запрос для получения новостей за определенный период времени.
        Максимальный период 30 дней."""
    # дополнительно сделал ограничения на кол-во дней по которым будет выдавать новости
    if period.end_period < period.start_period:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date of the period is less than the Start date",
        )
    elif (period.end_period - period.start_period).days > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The limit of the maximum number of days in the period has been exceeded. Max count day 30!",
        )
    query = select(news_model.c.title, news_model.c.date, news_model.c.url_picture).filter(news_model.c.date.between(
        period.start_period, period.end_period))
    news = await session.execute(query)
    return [NewsInfo(**new._mapping) for new in news]
