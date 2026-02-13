from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, boards, lists, cards

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(boards.router, prefix="/boards", tags=["boards"])
api_router.include_router(lists.router, prefix="", tags=["lists"])  # No prefix as routes have their own
api_router.include_router(cards.router, prefix="", tags=["cards"])  # No prefix as routes have their own
