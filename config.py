from dotenv import load_dotenv
import os


load_dotenv()

TABLE_NAME = 'labs_data'

DB_PARAMS = {
        'username': os.getenv('PG_USERNAME'),
        'password': os.getenv('PG_PASSWORD'),
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'dbname': os.getenv('PG_DBNAME')
    }

POSTGRES_URL = (
        f"postgresql+asyncpg://{DB_PARAMS['username']}:{DB_PARAMS['password']}@"
        f"{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
    )

SQLITE_URL = 'sqlite+aiosqlite:///static/data/labs.db'

