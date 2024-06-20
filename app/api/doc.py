from .base import *


router = fa.APIRouter(
    prefix="/doc",
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("/upload")
async def upload(
        user: str | None = None,
        file: fa.UploadFile = fa.File(...),
):
    res = define.Result()
    try:
        pass
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)

