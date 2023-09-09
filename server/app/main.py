from fastapi import FastAPI, Request, responses, status
from app.routers.users import user_router
from app.routers.bucket import bucket_router
from app.routers.stockslist import stock_list_render_router
from app.routers.kite import kite_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Define a middleware function to handle exceptions globally
async def exception_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        return responses.JSONResponse(
            content={"error": str(error)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Add the middleware to the app
app.middleware("http")(exception_handler)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(bucket_router, prefix="/bucket")
app.include_router(kite_router, prefix="/kite")
app.include_router(stock_list_render_router, prefix="/stock")
