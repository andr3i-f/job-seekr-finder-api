from typing import Union
from fastapi import FastAPI, Depends

from .dependencies import get_query_token
from .routes import items

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(items.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
