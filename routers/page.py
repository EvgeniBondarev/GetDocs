from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


from utils.repository import AioSqliteRepository


db = AioSqliteRepository("labs.db")

page_router = APIRouter(
    prefix="/page",
    tags=["Main record view"]
)
templates = Jinja2Templates(directory="templates")

@page_router.get("/index")
@page_router.get("/main")
@page_router.get("/")
async def redirect_page():
    return RedirectResponse("/page/1")

@page_router.get("/{page_number}",  response_class=HTMLResponse)
async def render_page(request: Request, page_number: int, record_count: int = 20):
    records = await db.get_records_in_range(page_number, record_count)
    all_record_count = await db.get_records_count()
    link_count = all_record_count // record_count

    return templates.TemplateResponse("page.html", {"request": request,
                                                    "records": records,
                                                    "all_record_count": all_record_count,
                                                    "link_count": link_count})




@page_router.post("/serch", response_class=HTMLResponse)
async def postdata(request: Request, serching_data=Form()):
    records = await db.full_text_search(serching_data)
    return templates.TemplateResponse("serch_page.html", {"request": request, "records": records})