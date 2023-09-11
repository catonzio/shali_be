from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
)
app.include_router(item_router, prefix="/api/v1/items")
app.include_router(lists_router, prefix="/api/v1/lists")
app.include_router(user_router, prefix="/api/v1/users")
app.include_router(access_router, prefix="/api/v1/auth")

origins = [
    "http://localhost:57113",  # Add your origins here
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
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
