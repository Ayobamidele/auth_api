from db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Organisation(Base):
	__tablename__ = "organisations"

	orgId = Column(String, primary_key=True, index=True)
	name = Column(String, nullable=False)
	description = Column(String, nullable=True)


class UserOrganisation(Base):
	__tablename__ = "user_organisation"

	user_id = Column(Integer, ForeignKey("users.userId"), primary_key=True)
	organisation_id = Column(String, ForeignKey("organisations.orgId"), primary_key=True)


