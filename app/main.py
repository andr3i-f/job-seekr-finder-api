from typing import Union
from fastapi import FastAPI, Depends
from fastapi_utilities import repeat_every

from .dependencies import get_query_token
from .routes import items

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(items.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
@repeat_every(seconds=3)
async def print_hello():
    print("hello world")