from .base import *


router = fa.APIRouter(
    prefix="/knowledge",
    tags=["Knowledge", ],
    dependencies=[
        # fa.Depends(shared.token.request),
    ],
)


@router.post("/type")
async def post_knowledge_type(
        req: define.knowledge.AddKlTypeReq
):
    res = define.Result()
    try:
        service.knowledge.type_.add(
            req=req
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.delete("/type")
async def delete_knowledge_type(
        id: str | int
):
    res = define.Result()
    try:
        service.knowledge.type_.delete(
            id_=id,
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.get("/type/list")
async def get_knowledge_type_list(
        page_no: int | None = 1,
        page_size: int | None = 30,
):
    res = define.Result()
    try:
        total, list_ = service.knowledge.type_.list_(
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


@router.get("/doc/list")
async def get_knowledge_doc_list(
        page_no: int | None = 1,
        page_size: int | None = 30,
):
    res = define.Result()
    try:
        total, list_ = service.knowledge.doc.list_(
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


@router.post("/doc")
async def post_knowledge_doc(
        req: define.knowledge.AddKlDocReq,
):
    res = define.Result()
    try:
        service.knowledge.doc.add(
            req=req
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.post("/doc/reset")
async def post_knowledge_doc_reset(
        req: define.knowledge.ResetDocReq
):
    res = define.Result()
    try:
        service.knowledge.doc.embedding(
            id_=req.id,
            chunk_size=req.chunk_size,
            override_size=req.override_size,
            insert=True,
        )
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


@router.get("/reset")
async def post_knowledge_reset(
        id: str | int,
):
    res = define.Result()
    try:
        ret = service.knowledge.reset(
            id_=id,
        )
        res.data = ret
    except Exception as ex:
        res.code = -1
        res.msg = str(ex)
    return res


shared.router.include_router(
    router=router
)

