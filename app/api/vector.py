from .base import *


router = fa.APIRouter(
    prefix="/vector",
    tags=["Vector", ],
)


@router.post("")
async def post_vector(
        req: define.vector.AddVectorReq
):
    res = define.Result()
    try:
        service.vector.add(
            req=req,
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)
