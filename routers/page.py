from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from utils.repository import DatabaseType
from utils.managers import DatabaseManager


db_manager = DatabaseManager(db_type=DatabaseType.POSTGRES, connection_string="postgres://nqecpchjjsqvar:aaee867229edb60c7e368f06d4a204e1a624e439c1f7a218cb14cb0aff10e9a7@ec2-52-215-68-14.eu-west-1.compute.amazonaws.com:5432/d28hr60skva2i5")
db = db_manager.get_repository()

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
def render_page(request: Request, page_number: int, record_count: int = 20):
    records = db.get_records_in_range(page_number, record_count)
    all_record_count = db.get_records_count()
    link_count = all_record_count // record_count

    return templates.TemplateResponse("page.html", {"request": request,
                                                    "page_number": page_number,
                                                    "records": records,
                                                    "all_record_count": all_record_count,
                                                    "link_count": link_count})



@page_router.post("/serch", response_class=HTMLResponse)
def postdata(request: Request, serching_data=Form()):
    records = db.full_text_search(serching_data)
    return templates.TemplateResponse("serch_page.html", {"request": request, "records": records})