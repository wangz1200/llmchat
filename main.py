from app import shared
from app import service
import uvicorn


if __name__ == "__main__":
    service.init()
    host = shared.config.args["server"]["host"]
    port = shared.config.args["server"]["port"]
    uvicorn.run(
        app=shared.router,
        host=host,
        port=port,
    )
 