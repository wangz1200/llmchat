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
    return EventSourceResponse(service.chat.chat(
        messages=req.messages,
    ))


@router.post("/agent")
async def chat_agent():
    return None


shared.router.include_router(
    router=router
)

