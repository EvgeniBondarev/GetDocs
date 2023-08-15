from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from routers.page import page_router


app = FastAPI(
    title="GetDocsAPI"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(
    page_router
)

@app.get("/")
def to_main():
    return RedirectResponse("/page")