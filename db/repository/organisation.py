from sqlalchemy.orm import Session 
from schemas.organisation import CreateOrganisation
from db.models.organisation import Organisation
import uuid



def generate_unique_organization_id():
	"""
	Generates a unique organization ID using UUID.

	Returns:
		str: A unique organization ID.
	"""
	return str(uuid.uuid4())

def create_new_organisation(organisation: CreateOrganisation, db: Session):	
	generated_id = generate_unique_organization_id()
	existing_org = db.query(Organisation).filter_by(name=organisation.name).first()

	if existing_org:
		return existing_org
	else:
		# Create new organisation
		organisation = Organisation(**organisation.dict(),orgId=generated_id)
		db.add(organisation)
		db.commit()
		db.refresh(organisation)
		return organisation


def retrieve_organisation(id: str, db: Session):
	organisation = db.query(Organisation).filter(Organisation.orgId == id).first()
	return organisation


def get_organisation(name: str, db: Session):
	organisation = db.query(Organisation).filter(Organisation.name == name).first()
	return organisation


def list_organisations(db : Session):
	organisations = db.query(Organisation).all()
	return organisations
