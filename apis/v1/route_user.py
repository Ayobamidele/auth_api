from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter, status
from db.session import get_db
from schemas.user import UserCreate
from db.repository.user import create_new_user
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from util.util import process_error
from core.security import create_access_token


router = APIRouter()



@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: Session = Depends(get_db)):
	try:
		user = create_new_user(payload.dict(), db=db)
		token = create_access_token({'sub': user.email})
		return {
			"status": "success",
			"message": "Registration successful",
			"data": {
				"accessToken": token,
				"user": {
					"userId": user.userId,
					"firstName": user.firstName,
					"lastName": user.lastName,
					"email": user.email,
					"phone": user.phone,
				}
			}
		}
	except Exception as error:
		if error.status_code == 422:
			return JSONResponse(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			content=jsonable_encoder({
				"errors": [
						{
							"field": "email",
							"message": "Email already exists."
						}
				]
			}),
		)
		elif error is RequestValidationError:
			return JSONResponse(
				jsonable_encoder({
					"errors": process_error(error.json())
				}),
				status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			)
		else:
			return JSONResponse(
				status_code=status.HTTP_400_BAD_REQUEST,
				content=jsonable_encoder({
					"status": "Bad request",
					"message": "Registration unsuccessful",
					"statusCode": 400
				}),
			)

