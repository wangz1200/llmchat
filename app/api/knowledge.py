from .base import *


router = fa.APIRouter(
    prefix="/knowledge",
    tags=["Knowledge", ],
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("/type")
async def post_knowledge_type(
        req: define.knowledge.AddKlTypeReq
):
    res = define.Result()
    try:
        data = req.data
        if not isinstance(data, list):
            data = [data, ]
        service.knowledge.type_.add(
            data=data
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.get("/type/list")
async def get_knowledge_type_list(
        req: define.knowledge.GetKlTypeListReq
):
    res = define.Result()
    return res


@router.post("/reset")
async def post_knowledge_reset(
        req: define.knowledge.ResetKlReq
):
    res = define.Result()
    try:
        ret = service.knowledge.reset(
            id_=req.id,
        )
        res.data = ret
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)

