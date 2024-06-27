from .base import *

router = fa.APIRouter(
    prefix="/chat",
    tags=["Chat", ],
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("")
async def post_chat(
        req: define.chat.ChatReq,
):
    if req.knowledge:
        return EventSourceResponse(service.chat.knowledge(
            req=req,
        ))
    else:
        return EventSourceResponse(service.chat.chat(
            req=req,
        ))


@router.post("/tool")
async def post_chat_tool(
        req: define.chat.ChatToolReq,
):
    return EventSourceResponse(service.chat.tool(
        req=req,
    ))


@router.post("/agent")
async def chat_agent():
    return None


shared.router.include_router(
    router=router
)
