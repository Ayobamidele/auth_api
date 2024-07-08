from sqlalchemy.orm import Session
from db.repository.organisation import create_new_organisation
from schemas.organisation import CreateOrganisation
from tests.utils.user import create_random_user
import uuid



def generate_unique_organization_id():
	"""
	Generates a unique organization ID using UUID.

	Returns:
		str: A unique organization ID.
	"""
	return str(uuid.uuid4())

def create_random_organisation(db: Session):
	user = create_random_user(db=db)
	org_name = f"{user.firstName}'s Organisation"
	organisation = CreateOrganisation(name=org_name, orgId=generate_unique_organization_id())
	organisation = create_new_organisation(organisation=organisation, db=db, user_id=user.id)
	user.organisations.append(organisation) 
	db.add(user)
	db.commit()
	db.refresh(user)
	return organisation