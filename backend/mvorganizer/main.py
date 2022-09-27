from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .base_db import engine
from .config import init
from .models import Base
from .routes import (
    actors_router,
    categories_router,
    movies_router,
    series_router,
    studios_router,
)

logger, config = init()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(?:127\.0\.0\.1|localhost):300[0-9]",
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(movies_router, prefix="/movies", tags=["movies"])
app.include_router(actors_router, prefix="/actors", tags=["actors"])
app.include_router(
    categories_router, prefix="/categories", tags=["categories"]
)
app.include_router(studios_router, prefix="/studios", tags=["studios"])
app.include_router(series_router, prefix="/series", tags=["series"])


@app.get("/")
def hello():
    return "Hello from FastAPI"
