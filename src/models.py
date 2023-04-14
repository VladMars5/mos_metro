from sqlalchemy import TIMESTAMP, Column, Integer, String, Table, Identity, Date
from database import metadata
from datetime import datetime

news = Table(
    "news",
    metadata,
    Column("id", Integer, Identity(), nullable=False, unique=True),
    Column("title", String(length=2048), nullable=False, primary_key=True),
    Column("date", Date, nullable=False),
    Column("url_picture", String(length=1024), nullable=False),
    Column("datetime_parse", TIMESTAMP, nullable=False, default=datetime.utcnow)
)
