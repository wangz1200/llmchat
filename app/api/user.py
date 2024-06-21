import fastapi

from .base import *


router = fastapi.APIRouter(
    prefix="/user",
    tags=["User", ],
)


@router.post("")
async def add_user(
        req: define.user.AddUserReq,
):
    pass


shared.router.include_router(
    router=router
)
