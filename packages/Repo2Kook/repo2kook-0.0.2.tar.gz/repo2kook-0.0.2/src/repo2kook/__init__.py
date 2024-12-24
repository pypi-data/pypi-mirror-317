from fastapi import FastAPI

app = FastAPI(docs_url=None)

from .middleware import VerifySignatureMiddleware
from .router import router

app.include_router(router)
app.add_middleware(VerifySignatureMiddleware)


def run():
    import uvicorn

    uvicorn.run(
        "repo2kook:app", host="0.0.0.0", port=3030, reload=True, log_level="info"
    )
