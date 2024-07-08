from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from db.session import get_db
from core.hashing import Hasher
from schemas.user import UserLogin
from db.repository.login import get_user
from core.security import create_access_token

router = APIRouter()

def authenticate_user(email: str, password: str,db: Session):
	user = get_user(email=email,db=db)
	if not user:
		return False
	if not Hasher.verify_password(password, user.password):
		return False
	return user


@router.post("/login")
def login(payload: UserLogin, db: Session= Depends(get_db)):
	user = authenticate_user(**payload.dict(),db=db)
	if not user:
		return JSONResponse(
			status_code=status.HTTP_401_UNAUTHORIZED,
			content=jsonable_encoder({
				"status": "Bad request",
				"message": "Authentication failed",
				"statusCode": 401
			})
   		)
			
	access_token = create_access_token(
		data={"sub": user.email}
	)
	return JSONResponse(
     		status_code=status.HTTP_200_OK,
       		content=jsonable_encoder({
				"status": "success",
				"message": "Login successful",
				"data": {
					"accessToken": access_token,
					"user": {
							"userId": user.userId,
							"firstName": user.firstName,
							"lastName": user.lastName,
							"email": user.email,
							"phone": user.phone,
						}
				}
			})
		)