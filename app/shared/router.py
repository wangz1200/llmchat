import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


__all__ = (
    "router"
)


router = fa.FastAPI()
router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router.add_middleware(
    SessionMiddleware,
    secret_key="secret_key"
)

