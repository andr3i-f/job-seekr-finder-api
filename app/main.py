from typing import Union
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from .dependencies import get_query_token
from .routes import items
from .scrapers.adzuna import Adzuna

load_dotenv()

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(items.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def start_scrapers():
    adzuna = Adzuna()

    await adzuna.start()
