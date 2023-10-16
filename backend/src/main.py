from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from controllers.item_controller import router as item_router
from controllers.list_controller import router as lists_router
from controllers.user_controller import router as user_router
from controllers.access_controller import router as access_router

from db import create_tables

app = FastAPI(
    title="ShaLi Backend",
    description="FastAPI Application backend for ShaLi",
    version="1.0.0",
    docs_url="/shali/api/docs",
    openapi_url="/shali/api/openapi.json",
)

app.include_router(item_router, prefix="/shali/api/items")
app.include_router(lists_router, prefix="/shali/api/lists")
app.include_router(user_router, prefix="/shali/api/users")
app.include_router(access_router, prefix="/shali/api/auth")

origins = [
    "http://localhost:63178",  # Add your origins here
    "http://localhost:80",
    "http://localhost:8000",
    "*"
    # "http://your.other.domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}
    )


@app.get("/")
async def root():
    return RedirectResponse(url="/shali/api")


@app.get("/shali/api")
async def root_shali():
    return RedirectResponse(url="/shali/api/docs")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
