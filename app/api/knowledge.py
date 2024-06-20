from .base import *


router = fa.APIRouter(
    prefix="/knowledge",
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("/reset")
async def post_knowledge_reset(
        req: define.knowledge.ResetKnowledgeReq
):
    res = define.Result()
    try:
        ret = service.knowledge.reset()
        res.data = ret
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)

