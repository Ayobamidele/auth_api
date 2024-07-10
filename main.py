from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
from util.util import process_error
from fastapi.encoders import jsonable_encoder
from core.config import settings
from db.session import engine 
from db.base import Base
from apis.base import api_router


def include_router(app):   
	app.include_router(api_router)

def create_tables():         
	Base.metadata.create_all(bind=engine)
		
def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	create_tables()
	include_router(app)
	return app


app = start_application()



@app.get("/")
def home():
	return {
		"message": "Hey There👋. Welcome to Auth API. By Ayobamidele Ewetuga @ https://github.com/Ayobamidele"
	}


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
	return JSONResponse(
		content=jsonable_encoder(process_error(exc.errors())),
		status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
	)

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(process_error(exc.errors())),
    )