from .base import *


router = fa.APIRouter(
    prefix="/doc",
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


shared.router.include_router(
    router=router
)

