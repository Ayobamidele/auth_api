from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette import status
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from schemas.user import UserCreate
from db.models.user import User
from db.models.organisation import Organisation 
from core.hashing import Hasher
import uuid




def generate_unique_organization_id():
	"""
	Generates a unique organization ID using UUID.

	Returns:
		str: A unique organization ID.
	"""
	return str(uuid.uuid4())


def create_new_user(user:UserCreate,db:Session):
	existing_email = db.query(User).filter_by(email=user['email']).first()
	if existing_email:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail=jsonable_encoder({
				"errors": [
						{
							"field": "email",
							"message": "Email already exists."
						}
				]
			}),
		)
	

	user = User(
		firstName = user['firstName'], 
		lastName = user['lastName'], 
		email = user['email'],
		password=Hasher.get_password_hash(user['password']),
		phone=user.get('phone',"")
	)
	
	# Create organisation
	org_name = f"{user.firstName}'s Organisation"
	generated_id = generate_unique_organization_id()
	existing_org = db.query(Organisation).filter_by(orgId=generated_id).first()

	if existing_org:
		organisation = existing_org
	else:
		# Create new organisation
		organisation = Organisation(orgId=generated_id, name=org_name)
		db.add(organisation)


	user.organisations.append(organisation)
 
	db.add(user)
	db.add(organisation)
	db.commit()
	db.refresh(user)
	db.refresh(organisation)
	return user