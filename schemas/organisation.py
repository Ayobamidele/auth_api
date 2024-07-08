from typing import Optional
from pydantic import BaseModel
from datetime import date




class CreateOrganisation(BaseModel):
	name: str 
	description: Optional[str] = "" 


class AddToOrganisation(BaseModel):
	userId: int 
		
class ShowOrganisation(BaseModel):
	orgId: str 
	name: str 
	description: Optional[str] = ""  

	class Config():
		from_attributes = True