from fastapi import APIRouter, status, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import JSONResponse
from starlette import status
from db.session import get_db
from schemas.organisation import CreateOrganisation, AddToOrganisation
from db.repository.organisation import create_new_organisation, retrieve_organisation, list_organisations
from fastapi.encoders import jsonable_encoder
from db.models.user import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db.repository.login import get_user, get_user_id
from core.config import settings
from db.models.user import User
from db.models.organisation import UserOrganisation
from schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from core.hashing import Hasher
from core.security import create_access_token 

router = APIRouter()

def authenticate_user(username: str, password: str, db: Session):
	user = get_user(email=username, db=db)
	if not user:
		return False
	if not Hasher.verify_password(password, user.password):
		return False
	return user



@router.post("/token", response_model=Token)
def login_for_access_token(
	 form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
	user = authenticate_user(form_data.username, form_data.password, db)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
		)
	access_token = create_access_token(data={"sub": user.email})
	return {"access_token": access_token, "token_type": "bearer"}
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail={
							"status": "Bad request",
							"message": "Authentication failed",
							"statusCode": 401
				}
	)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		email: str = payload.get("sub")
		if email is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	user = get_user(email=email, db=db)
	if user is None:
		raise credentials_exception
	return user



@router.get("/users/{id}")
def get_user_data(id: int, current_user: User=Depends(get_current_user), db: Session= Depends(get_db)):
	user = current_user
	if user.userId == id:
		return JSONResponse(
				status_code=status.HTTP_200_OK,
				content=jsonable_encoder({
						"status": "success",
						"message": f"Welcome {user.firstName}",
						"data": {
							"userId": user.userId,
							"firstName": user.firstName,
							"lastName": user.lastName,
							"email": user.email,
							"phone": user.phone
						}
					})
				)
	else:
		user = get_user_id(id, db=db)
		current_user_organisations = [i.orgId for i in current_user.organisations]
		for i in current_user_organisations:
			exists = db.query(UserOrganisation).filter(UserOrganisation.organisation_id == i, UserOrganisation.user_id == user.userId).first()
			if exists:
				return JSONResponse(
						status_code=status.HTTP_200_OK,
						content=jsonable_encoder({
								"status": "success",
								"message": f"Welcome {user.firstName}",
								"data": {
									"userId": user.userId,
									"firstName": user.firstName,
									"lastName": user.lastName,
									"email": user.email,
									"phone": user.phone
								}
							})
						)
		return JSONResponse(
		status_code=status.HTTP_200_OK,
		content=jsonable_encoder({
				"status": "success",
				"message": f"Welcome {current_user.firstName}",
				"data": {
					"userId": current_user.userId,
					"firstName": current_user.firstName,
					"lastName": current_user.lastName,
					"email": current_user.email,
					"phone": current_user.phone
				}
			})
  		) 


# Create Organisation
@router.post("/organisations")
def create_organisation(organisation: CreateOrganisation, current_user: User=Depends(get_current_user), db: Session= Depends(get_db)):
	organisation = create_new_organisation(organisation=organisation,db=db)
	if organisation:
		current_user.organisations.append(organisation)
		db.add(current_user)
		db.commit()
		return JSONResponse(
			status_code=status.HTTP_200_OK,
			content=jsonable_encoder(
				{
					"status": "success",
					"message": "Organisation created successfully",
					"data": {
							"orgId": organisation.orgId, 
							"name": organisation.name, 
							"description": organisation.name
						}
				}
			))
	else:
		return JSONResponse(
			status_code=status.HTTP_200_OK,
			content=jsonable_encoder(
						{
					"status": "Bad Request",
					"message": "Client error",
					"statusCode": 400
				}
			))
     

# Get all Organisatons
@router.get("/organisations" )
def get_organisations(current_user: User=Depends(get_current_user), db: Session= Depends(get_db)):
	organisations = list_organisations(db=db)
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content=jsonable_encoder({
			"status": "success",
			"message": "Here's all your organisations.",
			"data": {
				"organisations": organisations
			}
		}))

# Get one Organisation
@router.get("/organisations/{orgId}")
def get_organisation(orgId: str, current_user: User=Depends(get_current_user), db: Session= Depends(get_db)):
	organisation = retrieve_organisation(id=orgId, db=db)
	if not organisation:
		return JSONResponse(
		status_code=status.HTTP_404_NOT_FOUND,
		content=jsonable_encoder({
			"status": "Bad request",
			"message": f"Organisation with ID {orgId} does not exist.",
		}))
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content=jsonable_encoder({
			"status": "success",
			"message": f"Welcome to {organisation.name}.",
			"data": {
				"orgId": organisation.orgId,
				"name": organisation.name, 
				"description": organisation.description,
			}
		}))


@router.post("/organisations/{orgId}/users")
def add_user_to_organisation(orgId: str, userID: AddToOrganisation, db: Session= Depends(get_db)):
	user = get_user_id(userID.userId, db=db)
	organisation = retrieve_organisation(id=orgId, db=db)
	user.organisations.append(organisation)
	db.add(user)
	db.commit()
	return JSONResponse(
		status_code=status.HTTP_200_OK,
		content=jsonable_encoder({
				"status": "success",
				"message": "User added to organisation successfully",
		}))

