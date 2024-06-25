from .base import *


router = fa.APIRouter(
    prefix="/doc",
    tags=["Doc", ],
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("/file")
async def post_doc(
        req: define.doc.AddDocFileReq
):
    res = define.Result()
    try:
        service.doc.file.add(
            req=req
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.put("/file")
async def put_doc(
        req: define.doc.UpdateDocFileReq,
):
    res = define.Result()
    return res


@router.get("/file/list")
async def get_doc_file_list(
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


@router.post("/file/upload")
async def post_doc_upload(
        file: fa.UploadFile = fa.File(...),
):
    pass


@router.post("/file/embedding")
async def post_doc_embedding(
        req: define.doc.EmbDocFileReq,
):
    res = define.Result()
    try:
        service.doc.file.embedding(
            req=req
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.post("/folder")
async def post_doc_folder(
        req: define.doc.AddDocFolderReq
):
    res = define.Result()
    return res


@router.put("/folder")
async def put_doc_folder(
        req: define.doc.UpdateDocFolderReq
):
    res = define.Result()
    return res


shared.router.include_router(
    router=router
)

