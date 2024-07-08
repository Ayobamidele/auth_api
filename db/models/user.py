from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base


class User(Base):
	__tablename__ = "users"
	__table_args__ = {"extend_existing": True}
	
	userId = Column(Integer, primary_key=True, nullable=False, index=True)
	firstName = Column(String, nullable=False)
	lastName = Column(String, nullable=False)
	email = Column(String, nullable=False, unique=True)
	password = Column(String, nullable=False)
	phone = Column(String)
	organisations = relationship("Organisation", secondary="user_organisation")


