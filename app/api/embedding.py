from .base import *


router = fa.APIRouter(
    prefix="/embedding",
    tags=["embedding", ],
)


@router.post("/encode")
async def post_embedding_code(
        req: define.embedding.EmbeddingEncodeReq
):
    res = define.Result()
    try:
        data = service.embedding.encode(
            text=req.text,
        )
        res.data = data
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router,
)