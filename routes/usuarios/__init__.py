from fastapi import APIRouter
from .create_user import router as create_user_router
from .get_contact import router as get_contact_router
from .assign_role import router as assign_role_router

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])

usuarios_router.include_router(create_user_router)
usuarios_router.include_router(get_contact_router)
usuarios_router.include_router(assign_role_router)