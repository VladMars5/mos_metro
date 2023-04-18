from pydantic import BaseModel, validator, Field
from datetime import date
from typing import Optional


class NewsInfo(BaseModel):
    title: str
    date: date
    url_picture: Optional[str] = ''


class NewsPeriod(BaseModel):
    start_period: date = Field(default_factory=date.today)
    end_period: date = Field(default_factory=date.today)

    @validator('end_period', always=True)
    def passwords_match(cls, v, values):
        if v < values.get('start_period'):
            raise ValueError("End date of the period is less than the Start date")
        elif (v - values.get('start_period')).days > 30:
            raise ValueError("The limit of the maximum number of days in the period has been exceeded. "
                             "Max count day 30!")
        return v
