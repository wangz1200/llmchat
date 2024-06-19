from app import shared
import uvicorn


if __name__ == "__main__":
    host = shared.config.args["server"]["host"]
    port = shared.config.args["server"]["port"]
    uvicorn.run(
        app=shared.router,
        host=host,
        port=port,
    )
 