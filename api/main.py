from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from api.config.settings import settings
from api.core.logging import setup_logging
from api.core.container import Container
import uvicorn

setup_logging()

container = Container()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for automating PostgreSQL primary-replica setup",
    version=settings.VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

from api.routes import infrastructure
app.include_router(
    infrastructure.router,
    prefix=f"{settings.API_V1_STR}/infrastructure",
    tags=["infrastructure"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=4
    )
