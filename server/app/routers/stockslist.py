from fastapi import APIRouter, Depends, Request
from app.models.requests.user_schemas import User
from app.utils.jwt import get_current_user
from app.services.fmp_nasdaq.stockslist import StocksList as StockListNasdaq
from app.services.fmp_nasdaq.stock import Stock as StockNasdaq

from app.services.fmp_nse.stockslist import StocksList as StockListNse
from app.services.fmp_nse.stock import Stock as StockNse

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

stock_list_render_router = APIRouter()


@stock_list_render_router.get("/list", response_model=None)
async def get_all_stocks(
    stock_index: str, current_user: User = Depends(get_current_user)
):
    """
    return stock list.
    """
    stocks = []

    if stock_index == "nasdaq":
        stock_list = StockListNasdaq()
        stocks = stock_list.get_stock_list()

    if stock_index == "nse":
        stock_list = StockListNse()
        stocks = stock_list.get_stock_list()

    return stocks


@stock_list_render_router.get("/render")
def render_stock_jinja(stock_code: str, request: Request):
    """
    render stock using jinja template and highcharts.
    """
    return templates.TemplateResponse(
        "index.html", {"request": request, "stock_code": stock_code}
    )


@stock_list_render_router.get("/renderdata")
async def render_stock(stock_index: str, stock_code: str):
    """ 
    render stock using react and highcharts.    
    """

    response = None

    if stock_index == "nasdaq":
        stock = StockNasdaq(stock_code)
    if stock_index == "nse":
        stock = StockNse(stock_code)

    response = stock.render_data()
    return response
