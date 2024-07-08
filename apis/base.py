from fastapi import APIRouter
from apis.v1 import route_user, route_organisation, route_login

api_router = APIRouter()
api_router.include_router(route_user.router,prefix='/auth',tags=['Auth'])
api_router.include_router(route_organisation.router,prefix='/api',tags=['Api'])
api_router.include_router(route_login.router, prefix='/auth',tags=['Auth'])