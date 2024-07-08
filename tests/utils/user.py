from sqlalchemy.orm import Session
from db.repository.user import create_new_user
from schemas.user import UserCreate

data = {
		"firstName": "Mark",
		"lastName": "Test",
		"email":"testuser@hng.com",
		"password":"testing123",
		"phone": "0913277789"
	}

def create_random_user(db: Session):
    user = UserCreate(**data)
    user = create_new_user(user=user, db=db)
    return user