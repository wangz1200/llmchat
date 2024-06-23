from .base import *


router = fa.APIRouter(
    prefix="/user",
    tags=["User", ],
)


@router.post("")
async def post_user(
        req: define.user.AddUserReq,
):
    res = define.Result()
    try:
        service.user.add(
            data=req.data,
            update=req.update
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)
