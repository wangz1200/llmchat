from .base import *


router = fa.APIRouter(
    prefix="/doc",
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.get("/list")
async def doc_list(
        id: str | int | None = None,
        pid: str | int | None = None,
        page_no: int = 1,
        page_size: int = 30,
):
    res = define.Result()
    try:
        pass
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.get("/download")
async def doc_download(
        id: str | int,
):
    pass


@router.post("/upload")
async def doc_upload(
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

