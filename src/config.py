import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

LIVE_POOL_DB_CONNECTIONS = int(os.environ.get("LIVE_POOL_DB_CONNECTIONS"))
COUNT_MAX_CONNECTIONS_DB = int(os.environ.get("COUNT_MAX_CONNECTIONS_DB"))
COUNT_OVERFLOW_POOL = int(os.environ.get("COUNT_OVERFLOW_POOL"))
