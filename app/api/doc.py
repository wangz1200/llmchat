from .base import *


router = fa.APIRouter(
    prefix="/doc",
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("")
async def upload(
        req: define.doc.UploadDoctReq,
):
    res = define.Result()
    try:
        pass
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.post("/knowledge")
async def chat_knowledge(
        req: define.chat.ChatKnowledgeReq
):
    pass


@router.post("/agent")
async def chat_agent():
    return None


shared.router.include_router(
    router=router
)

