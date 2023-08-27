from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from routers import page
from utils.db.database_client import DatabaseClient
from utils.db.database_type import DatabaseType


app = FastAPI(
    title="GetDocsAPI"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

page.db = DatabaseClient(DatabaseType.sqlite)

app.include_router(
    page.page_router
)

@app.get("/")
def to_main():
    return RedirectResponse("/page")