from base import *


router = fa.APIRouter(
    prefix="/chat"
)


@router.post("")
async def chat_chat(
        req: define.chat.ChatReq,
):
    return EventSourceResponse(service.chat.chat(
        messages=req.messages,
    ))


@router.post("/knowledge")
async def chat_knowledge(
        req: define.chat.ChatKnowledgeReq
):
    pass


shared.router.include_router(
    router=router
)

