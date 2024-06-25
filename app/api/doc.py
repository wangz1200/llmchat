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
    try:
        service.doc.file.update(
            req=req
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.get("/file/list")
async def get_doc_file_list(
        page_no: int = 1,
        page_size: int = 30,
):
    res = define.Result()
    try:
        total, list_ = service.doc.file.list_(
            page_no=page_no,
            page_size=page_size,
        )
        res.data = {
            "total": total,
            "list": list_,
        }
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
    try:
        service.doc.folder.add(
            req=req
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.put("/folder")
async def put_doc_folder(
        req: define.doc.UpdateDocFolderReq
):
    res = define.Result()
    return res


@router.delete("/folder")
async def delete_doc_folder(
        id: str | int,
):
    res = define.Result()
    try:
        service.doc.folder.remove(
            id_=id
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.get("/folder/list")
async def get_doc_folder_list(
        id: str | int | None = None,
        page_no: int = 1,
        page_size: int = 30,
):
    res = define.Result()
    try:
        total, list_ = service.doc.folder.list_(
            id_=id,
            page_no=page_no,
            page_size=page_size,
        )
        res.data = {
            "total": total,
            "list": list_,
        }
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)

