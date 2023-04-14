from pydantic import BaseModel
from datetime import date
from typing import Optional


class NewsInfo(BaseModel):
    title: str
    date: date
    url_picture: Optional[str] = ''


class NewsPeriod(BaseModel):
    start_period: date = date.today()
    end_period: date = date.today()
