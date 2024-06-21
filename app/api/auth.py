from .base import *


router = fa.APIRouter(
    prefix="/auth",
    tags=["Auth", ],
)


@router.post("")
async def post_auth_login(
        req: define.auth.LoginReq
):
    res = define.Result()
    try:
        user = req.user
        password = req.password
        ret = service.auth.login(
            user_=user,
            password=password,
        )
        res.data = ret
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)

